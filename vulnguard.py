#!/usr/bin/env python3
"""
@file vulnguard.py
@brief A tool for analyzing code vulnerabilities using Ollama models.
"""

import ollama  # Ollama Python client
from collections import OrderedDict
from src.cve import Cve
from src.compute import compute
from src.database import Database
from src.parsing import parse
from tools.logger import PrettyLogger
import asyncio

logger = PrettyLogger("Vulnguard")

def list_ollama_models():
    """
    @brief Lists available Ollama models on the system.

    This function retrieves the list of available Ollama models and their metadata.
    It handles different response formats and logs the process.

    @return An OrderedDict mapping model names to their metadata.
    """

    logger.logger.info("Listing available Ollama models...")

    try:
        response = ollama.list()
        models = response.get('models', [])

        # Handle direct response list
        if not models and isinstance(response, list):
            models = response

        model_dict = OrderedDict()

        for model in models:
            if hasattr(model, 'model'):
                # Handle Model object
                model_name = model.model
                model_dict[model_name] = {
                    'modified_at': getattr(model, 'modified_at', 'Unknown date'),
                    'size': getattr(model, 'size', 'Unknown size'),
                    'details': getattr(model, 'details', {})
                }
            elif isinstance(model, dict):
                # Handle dictionary format
                model_name = model.get('name')
                if model_name:
                    model_dict[model_name] = {
                        'tag': model.get('tag', 'latest'),
                        'size': model.get('size', 'Unknown size'),
                        'modified_at': model.get('modified_at', 'Unknown date')
                    }

        return model_dict

    except Exception as e:
        logger.logger.error(f"Error while listing Ollama models: {str(e)}")
        return OrderedDict()


def ollama_prettylisting(models_dict):
    """
    @brief Prints a list of available Ollama models.

    This function prints the names of available Ollama models in a numbered list format.

    @param models_dict An OrderedDict containing model names and their metadata.
    """
    print("\nAvailable Ollama Models:")
    for idx, (model_name, _) in enumerate(models_dict.items(), 1):
        print(f"{idx}. {model_name}")


def choose_llm_model():
    """
    @brief Allows the user to choose an LLM model from the available Ollama models.

    This function lists available Ollama models and prompts the user to select one.
    It handles user input and defaults to a specified model if no valid selection is made.

    @return The name of the selected LLM model.
    """

    try:
        models_dict = list_ollama_models()
    except Exception as e:
        logger.logger.error(f"Error while initializing Ollama: {str(e)}")
        logger.logger.error("Please ensure Ollama is installed and running.")
        exit(1)

    if not models_dict:
        logger.logger.error("No Ollama models found. Please ensure Ollama is installed and running.")
        exit(1)

    ollama_prettylisting(models_dict)

    default_model = "Michel:latest"
    selected_model = default_model if default_model in models_dict else next(iter(models_dict.keys()), None)

    if not selected_model:
        logger.logger.error("No models available. Please add models to Ollama.")
        exit(1)

    print(f"\nDefault model: {selected_model}")
    model_choice = input("Select model (number or name, press Enter for default): ").strip()

    if model_choice:
        try:
            if model_choice.isdigit() and 1 <= int(model_choice) <= len(models_dict):
                selected_model = list(models_dict.keys())[int(model_choice) - 1]
            elif model_choice in models_dict:
                selected_model = model_choice
            else:
                logger.logger.warning(f"Invalid selection. Using default model: {selected_model}")
        except (ValueError, IndexError):
            logger.logger.warning(f"Invalid selection. Using default model: {selected_model}")

    return selected_model


def vulnguard():
    """
    @brief Main function that runs the VulnGuard vulnerability analysis tool.

    This function initializes the tool, allows the user to select an LLM model,
    and repeatedly prompts for CVE IDs and diff file locations to analyze vulnerabilities.
    """

    logger.logger.info("Starting Vulnguard vulnerability analysis tool")
    db = Database()

    selected_model = choose_llm_model()
    logger.logger.info(f"Selected model: {selected_model}")

    try:
        while True:
            cve_id = input("Enter CVE ID you want to analyze: ")
            diff_location = input("Enter the corresponding diff file location to analyze: ")

            cve_path = db.search(cve_id)
            cve = Cve(cve_id, cve_path)
            changes = parse(diff_location)

            asyncio.run(compute(cve, changes, selected_model))

            continue_choice = input("\nAnalyze another vulnerability? (y/n): ").lower()
            if continue_choice != 'y':
                logger.logger.info("Exiting Vulnguard")
                exit(0)

    except KeyboardInterrupt:
        print("\n")
        logger.logger.warning("Vulnguard terminated by user")
    except Exception as e:
        logger.logger.error(f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    vulnguard()
