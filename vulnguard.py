#!/usr/bin/env python3
"""
@file vulnguard.py
@brief A tool for analyzing code vulnerabilities using Ollama models
"""

import os
import sys
import json
import subprocess
from collections import OrderedDict
from src.cve import Cve
from src.database import Database
from tools.logger import PrettyLogger
import ollama  # Ollama Python client


def list_ollama_models():
    """
    List available Ollama models on the system.

    @return Dictionary mapping model names to their metadata
    """
    logger = PrettyLogger("ModelLister")
    logger.logger.info("Listing available Ollama models...")

    try:
        response = ollama.list()
        models = response.get('models', [])

        # If models isn't a list but rather the direct response, use it directly
        if not models and isinstance(response, list):
            models = response

        model_dict = OrderedDict()

        for model in models:
            # Handle both dictionary and Model object formats
            if hasattr(model, 'model'):
                # It's a Model object
                model_name = model.model
                model_dict[model_name] = {
                    'modified_at': getattr(model, 'modified_at', 'Unknown date'),
                    'size': getattr(model, 'size', 'Unknown size'),
                    'details': getattr(model, 'details', {})
                }
            elif isinstance(model, dict):
                # It's a dictionary
                model_name = model.get('name')
                if model_name:
                    model_dict[model_name] = {
                        'tag': model.get('tag', 'latest'),
                        'size': model.get('size', 'Unknown size'),
                        'modified_at': model.get('modified_at', 'Unknown date')
                    }

        if not model_dict:
            logger.logger.warning("No Ollama models found. Is Ollama installed and running?")

        return model_dict

    except Exception as e:
        logger.logger.error(f"Error listing Ollama models: {str(e)}")
        logger.logger.error("Make sure Ollama service is running")
        return OrderedDict()



def format_prompt(cve_description, file_location, diff_hunk, template_path="../llm/user-prompt.txt"):
    """
    Format the prompt using the template and input parameters.

    @param cve_description Description of the CVE
    @param file_location Location of the file being analyzed
    @param diff_hunk The diff hunk to analyze
    @param template_path Path to the template file
    @return Formatted prompt string
    """
    logger = PrettyLogger("PromptFormatter")

    try:
        with open(template_path, 'r') as file:
            template = file.read()

        # Replace placeholders with actual values
        prompt = template.replace("{{CVE_DESCRIPTION}}", cve_description)
        prompt = prompt.replace("{{File_Location}}", file_location)
        prompt = prompt.replace("{{DIFF_HUNK}}", diff_hunk)

        return prompt
    except FileNotFoundError:
        logger.logger.error(f"Template file not found: {template_path}")
        logger.logger.info("Using default prompt format...")

        # Fallback to a simple built-in template
        prompt = f"""
You are a specialized code security assistant. Your task is to analyze the provided code diff hunk in the context of the CVE description given below.

Here is the CVE Description: {cve_description}
Here is the File location: {file_location}
Here is the Diff hunk: {diff_hunk}
"""
        return prompt


def analyze_vulnerability(model_name, prompt):
    """
    Send the prompt to the Ollama model for analysis.

    @param model_name Name of the Ollama model to use
    @param prompt Formatted prompt to send to the model
    @return Model's response
    """
    logger = PrettyLogger("VulnAnalyzer")

    try:
        logger.logger.info(f"Sending request to model: {model_name}")
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={
                "temperature": 0,  # Lower temperature for more deterministic responses
                "num_predict": 50000,  # Maximum token length for response
            }
        )
        return response.get('response', "No response received from model")
    except Exception as e:
        logger.logger.error(f"Error while querying the model: {str(e)}")
        return f"Error: {str(e)}"


def vulnguard():
    """
    Main function that runs the VulnGuard vulnerability analysis tool.
    """
    logger = PrettyLogger("Vulnguard")
    logger.logger.info("Starting Vulnguard vulnerability analysis tool")

    # Check if Ollama is installed and running
    try:
        models_dict = list_ollama_models()
        if not models_dict:
            logger.logger.error("No Ollama models found. Please ensure Ollama is installed and running.")
            return
    except Exception as e:
        logger.logger.error(f"Error initializing Ollama: {str(e)}")
        logger.logger.error("Please ensure Ollama is installed and running.")
        return

    # Print available models
    print("\nAvailable Ollama Models:")
    for idx, (model_name, _) in enumerate(models_dict.items(), 1):
        print(f"{idx}. {model_name}")

    # Select model (default to vulnerability_detector if available)
    default_model = "vulnerability_detector"
    selected_model = default_model if default_model in models_dict else next(iter(models_dict.keys()), None)

    if not selected_model:
        logger.logger.error("No models available. Please add models to Ollama.")
        return

    print(f"\nDefault model: {selected_model}")
    model_choice = input("Select model (number or name, press Enter for default): ").strip()

    if model_choice:
        try:
            # Check if input is a number
            if model_choice.isdigit() and 1 <= int(model_choice) <= len(models_dict):
                selected_model = list(models_dict.keys())[int(model_choice) - 1]
            # Check if input is a model name
            elif model_choice in models_dict:
                selected_model = model_choice
            else:
                logger.logger.warning(f"Invalid selection. Using default model: {selected_model}")
        except (ValueError, IndexError):
            logger.logger.warning(f"Invalid selection. Using default model: {selected_model}")

    logger.logger.info(f"Selected model: {selected_model}")

    # Main interaction loop
    try:
        while True:
            print("\n" + "=" * 50)
            print("VulnGuard Vulnerability Analysis")
            print("=" * 50)
            print("(Press Ctrl+C at any prompt to exit)")

            # Get inputs from user
            cve_description = input("\nEnter CVE Description: ").strip()
            file_location = input("Enter File Location: ").strip()
            print("Enter Diff Hunk (End with a line containing only 'END'): ")

            diff_lines = []
            while True:
                line = input()
                if line == "END":
                    break
                diff_lines.append(line)
            diff_hunk = "\n".join(diff_lines)

            # Format the prompt
            prompt = format_prompt(cve_description, file_location, diff_hunk)

            # Analyze vulnerability
            print("\nAnalyzing vulnerability... Please wait.")
            result = analyze_vulnerability(selected_model, prompt)

            # Display result
            print("\n" + "=" * 50)
            print("Analysis Result:")
            print("=" * 50)
            print(result)

            # Ask to continue
            continue_choice = input("\nAnalyze another vulnerability? (y/n): ").lower()
            if continue_choice != 'y':
                logger.logger.info("Exiting Vulnguard")
                break

    except KeyboardInterrupt:
        print("\n")
        logger.logger.info("Vulnguard terminated by user")
    except Exception as e:
        logger.logger.error(f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    vulnguard()