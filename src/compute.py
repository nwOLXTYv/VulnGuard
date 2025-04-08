"""
@file Compute.py
@brief Contains all functions and stuff related to ollama usage
"""

import os
import re
import time

import ollama

from enum import Enum
from src.cve import Cve
from src.parsing import GlobalChanges
from tools.logger import PrettyLogger

# User prompt template
user_prompt_template = "./docs/user-prompt.txt"
output_directory = "./output/"

logger = PrettyLogger("Compute")


class LlmOutput(Enum):
    """
    @enum LlmOutput
    @brief Enumeration representing possible outputs from the LLM analysis.

    This enumeration defines the possible outcomes of analyzing a diff hunk
    with respect to a CVE description.
    """
    VULNERABLE = 1  # The diff hunk is vulnerable.
    SAFE = 2        # The diff hunk is safe.
    ERROR = 3       # An error occurred during analysis.


def __format_prompt(cve_description, file_location, diff_hunk, template=user_prompt_template):
    """
    @brief Formats a prompt for the LLM using a template.

    This function reads a template file and replaces placeholders with actual data
    related to the CVE description, file location, and diff hunk. It logs the formatted
    prompt and handles file not found errors by using a default prompt format.

    @param cve_description The description of the CVE.
    @param file_location The location of the file being analyzed.
    @param diff_hunk The diff hunk to be analyzed.
    @param template The path to the prompt template file.

    @return A formatted prompt string.
    """

    try:
        with open(template, 'r') as file:
            user_prompt = file.read()

        user_prompt = user_prompt.replace("{{CVE_DESCRIPTION}}", cve_description)
        user_prompt = user_prompt.replace("{{File_Location}}", file_location)
        user_prompt = user_prompt.replace("{{DIFF_HUNK}}", diff_hunk)
        # logger.logger.info("Llm prompt: {}".format(user_prompt))

        return user_prompt

    except FileNotFoundError:
        logger.logger.error(f"Template file not found: {template}")
        logger.logger.info("Using default prompt format...")

        prompt = f"""
        You are a specialized code security assistant. Your task is to analyze the provided code diff hunk in the context of the CVE description given below.

        Here is the CVE Description: {cve_description}
        Here is the File location: {file_location}
        Here is the Diff hunk: {diff_hunk}
        """
        return prompt


async def __call_to_ollama(model_name, prompt):
    """
    @brief Sends a request to the Ollama model and retrieves the response.

    This function logs the request details and handles any exceptions that occur
    during the API call. It returns the model's response or an error message.

    @param model_name The name of the model to query.
    @param prompt The prompt to send to the model.

    @return The model's response or None if an error occurred.
    """

    try:
        logger.logger.info(f"Sending request to model: {model_name}")
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
        )
        return response.get('response', "No response received from model")
    except Exception as e:
        logger.logger.error(f"Error while querying the model: {str(e)}")
        return None


def __check_llm_output(llm_output):
    """
    @brief Checks the LLM output to determine if the diff hunk is vulnerable.

    This function analyzes the LLM's response to determine if the diff hunk is
    vulnerable, safe, or if an error occurred. It uses a regex pattern to identify
    safe responses.

    @param llm_output The output from the LLM.

    @return An LlmOutput enumeration value indicating the result.
    """
    if not llm_output:
        return LlmOutput.ERROR

    if re.search(r"/README.md", llm_output):
        return LlmOutput.SAFE

    pattern = r"The provided diff hunk does not contain code matching the CVE description"
    match = re.search(pattern, llm_output)
    if match:
        return LlmOutput.SAFE

    pattern2 = r"The provided diff hunk does not directly contain the vulnerable code for this vulnerability"
    match2 = re.search(pattern2, llm_output)
    if match2:
        return LlmOutput.SAFE

    return LlmOutput.VULNERABLE


def __save_llm_output(llm_output, file_name, diff_value):
    """
    @brief Saves the LLM output to a file.

    This function creates the necessary directories and saves the LLM output to a file.
    The file is named based on the provided file name and diff value, and is stored in
    a predefined output directory.

    @param llm_output The output from the LLM to be saved.
    @param file_name The name of the file associated with the LLM output.
    @param diff_value The diff value associated with the LLM output.
    """
    os.makedirs(os.path.dirname(output_directory), exist_ok=True)
    filename = os.path.join(output_directory, f"{file_name}_{diff_value}.txt")

    with open(filename, "w") as f:
        f.write(llm_output)


async def compute(cve: Cve, global_changes: GlobalChanges, model_name):
    """
    @brief Computes the vulnerability status of diff hunks in a set of files.

    This function iterates over the files and diff hunks in the GlobalChanges object,
    formats a prompt for each diff hunk, queries the LLM model, and checks the output
    to determine if the diff hunk is vulnerable. It logs the results and updates the
    CVE object with vulnerable code.

    @param cve The CVE object containing the description and code.
    @param global_changes The GlobalChanges object containing file and diff changes.
    @param model_name The name of the LLM model to query.
    """
    logger.logger.info("Starting computation...")
    f, d = 0, 0
    for file in global_changes.files:
        f += 1
        for diff in file.diffs:
            d += 1
            prompt = __format_prompt(cve.description, file.name, diff.value)
            begin = time.time()
            llm_output = await __call_to_ollama(model_name, prompt)
            end = time.time()
            logger.logger.info(f"Computation took {end - begin} seconds.")
            llm_result = __check_llm_output(llm_output)

            if llm_result == LlmOutput.ERROR:
                logger.logger.error(f"Error while querying the model...")
                continue
            if llm_result == LlmOutput.SAFE:
                logger.logger.info(f" Code in file: {file.name}, diff: {d} is not vulnerable.")
                continue
            if llm_result == LlmOutput.VULNERABLE:
                logger.logger.info(f"Vulnerable code found in file: {file.name}, diff: {d} !")
                cve.code.append((f, d))
                __save_llm_output(llm_output, f, d)

    logger.logger.info("Finished computation.")
    print(f"Llm output can be found in {output_directory}.")
