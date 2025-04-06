import re
import ollama

from enum import Enum
from src.cve import Cve
from src.parsing import GlobalChanges
from tools.logger import PrettyLogger

# User prompt template
user_prompt_template = "./docs/user-prompt.txt"


class LlmOutput(Enum):
    VULNERABLE = 1
    SAFE = 2
    ERROR = 3


def __format_prompt(cve_description, file_location, diff_hunk, template=user_prompt_template):
    logger = PrettyLogger("PromptFormatter")

    # Replace placeholders with actual data
    try:
        with open(template, 'r') as file:
            user_prompt = file.read()

        user_prompt = user_prompt.replace("{{CVE_DESCRIPTION}}", cve_description)
        user_prompt = user_prompt.replace("{{File_Location}}", file_location)
        user_prompt = user_prompt.replace("{{DIFF_HUNK}}", diff_hunk)
        logger.logger.info("Llm prompt: {}".format(user_prompt))

        return user_prompt

    except FileNotFoundError:
        logger.logger.error(f"Template file not found: {template}")
        logger.logger.info("Using default prompt format...")

        # Fallback to a simple built-in template
        prompt = f"""
    You are a specialized code security assistant. Your task is to analyze the provided code diff hunk in the context of the CVE description given below.

    Here is the CVE Description: {cve_description}
    Here is the File location: {file_location}
    Here is the Diff hunk: {diff_hunk}
    """
        return prompt


def __call_to_ollama(model_name, prompt):
    logger = PrettyLogger("CallToOllama")

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
    if not llm_output:
        return LlmOutput.ERROR

    pattern = r"The provided diff hunk does not contain code matching the CVE description"
    match = re.search(pattern, llm_output)
    if match:
        return LlmOutput.SAFE
    return LlmOutput.VULNERABLE


def compute(cve: Cve, global_changes: GlobalChanges, model_name):
    logger = PrettyLogger("Compute")
    f, d = 0, 0
    for file in global_changes.files:
        f += 1
        for diff in file.diff_hunks:
            d += 1
            prompt = __format_prompt(cve.description, file.name, diff.value)
            llm_output = __call_to_ollama(model_name, prompt)
            llm_result = __check_llm_output(llm_output)

            if llm_result == LlmOutput.ERROR:
                logger.logger.error(f"Error while querying the model...")
                continue
            if llm_result == LlmOutput.SAFE:
                logger.logger.info(f" Code in file: {file.name}, diff: {d} is not vulnerable.")
                continue
            if llm_result == LlmOutput.VULNERABLE:
                logger.logger.info(f"Vulnerable code found in file: {file.name}, diff: {d} !")
                cve.code.append(file.name + "\n" + diff.value + "\n")
