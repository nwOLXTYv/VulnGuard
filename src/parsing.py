"""
@file Parsing.py
@brief Contains all parsing function and classes related to diff files parsing
"""

import re
import sys

from tools.logger import PrettyLogger


class GlobalChanges:
    """
    @class GlobalChanges
    @brief Represents a collection of file changes parsed from a diff file.

    This class manages the parsing of diff content and stores the changes in a structured format.
    It contains methods to process file and diff changes and to extract relevant information from diff lines.
    """

    def __init__(self):
        """
        @brief Constructs a new GlobalChanges object.

        Initializes an empty list to store file changes.
        """
        self.files = []

    def parse_diff(self, diff_content):
        """
        @brief Parses the diff content and populates the GlobalChanges object.

        This method processes each line of the diff content to identify file and diff changes,
        and populates the GlobalChanges object accordingly.

        @param diff_content The content of the diff file as a string.
        """
        current_file = None
        current_diff = None

        lines = diff_content.splitlines()
        for line in lines:
            if self.is_new_file(line):
                current_file = self.process_new_file(line, current_file)
                current_diff = None
            elif FileChanges.is_new_diff(line):
                current_diff = current_file.process_new_diff(current_diff)
                current_diff.accumulate_content(line)  # Include the delimiter line
            elif current_diff is not None:
                current_diff.accumulate_content(line)

        self.finalize_parsing(current_file, current_diff)

    def process_new_file(self, line, current_file):
        """
        @brief Processes a new file change from a diff line.

        This method creates a new FileChanges object for the detected file change
        and appends the previous file change to the list if it exists.

        @param line The diff line indicating a new file change.
        @param current_file The current FileChanges object being processed.

        @return A new FileChanges object for the detected file change.
        """
        if current_file:
            self.files.append(current_file)
        file_name = self.extract_file_name(line)
        return FileChanges(file_name)

    def finalize_parsing(self, current_file, current_diff):
        """
        @brief Finalizes the parsing process by appending the last file and diff changes.

        This method ensures that the last processed file and diff changes are appended
        to their respective lists after the parsing loop.

        @param current_file The current FileChanges object being processed.
        @param current_diff The current DiffChanges object being processed.
        """
        if current_file:
            if current_diff:
                current_file.diffs.append(current_diff)
            self.files.append(current_file)

    @staticmethod
    def is_new_file(line):
        """
        @brief Checks if a line indicates a new file change.

        This method returns True if the line starts with "diff --git", indicating a new file change.

        @param line The diff line to check.
        @return True if the line indicates a new file change, False otherwise.
        """
        return line.startswith("diff --git")

    @staticmethod
    def extract_file_name(line):
        """
        @brief Extracts the file name from a diff line.

        This method uses a regular expression to extract the file name from a line
        that starts with "diff --git".

        @param line The diff line containing the file name.
        @return The extracted file name, or None if not found.
        """
        file_name_match = re.search(r'diff --git a/(.+?) b/', line)
        if file_name_match:
            return file_name_match.group(1)
        return None


class FileChanges:
    """
    @class FileChanges
    @brief Represents changes within a specific file in a diff.

    This class stores the name of the file and a list of diffs within that file.
    It provides methods to process new diffs and check for diff delimiters.
    """

    def __init__(self, name):
        """
        @brief Constructs a new FileChanges object.

        @param name The name of the file.
        """
        self.name = name
        self.diffs = []

    def process_new_diff(self, current_diff):
        """
        @brief Processes a new diff change within the file.

        This method creates a new DiffChanges object for the detected diff change
        and appends the previous diff change to the list if it exists.

        @param current_diff The current DiffChanges object being processed.
        @return A new DiffChanges object for the detected diff change.
        """
        if current_diff:
            self.diffs.append(current_diff)
        return DiffChanges()

    @staticmethod
    def is_new_diff(line):
        """
        @brief Checks if a line indicates a new diff change.

        This method returns True if the line matches the pattern
        @@ -{numbers},{numbers} +{numbers},{numbers} @@, indicating a new diff change.

        @param line The diff line to check.
        @return True if the line indicates a new diff change, False otherwise.
        """
        return bool(re.match(r'@@ -\d+,\d+ \+\d+,\d+ @@ +?', line))


class DiffChanges:
    """
    @class DiffChanges
    @brief Represents the content of a specific diff within a file.

    This class stores the diff content as a string and provides a method to accumulate diff lines.
    """

    def __init__(self):
        """
        @brief Constructs a new DiffChanges object.
        """
        self.value = ""

    def accumulate_content(self, line):
        """
        @brief Accumulates diff content by appending lines.

        This method appends a line to the diff content, including a newline character.

        @param line The diff line to append.
        """
        self.value += line + "\n"


def parse(diff_filename):
    """
    @brief Parses a diff file and returns a GlobalChanges object.

    This function reads the content of a diff file, parses it using the GlobalChanges class,
    and returns the populated GlobalChanges object. It handles file not found errors gracefully.

    @param diff_filename The path to the diff file.
    @return A GlobalChanges object containing the parsed diff data.
    """
    logger = PrettyLogger("GlobalChanges")
    logger.logger.info("Started parsing ...")
    try:
        with open(diff_filename, 'r', encoding="utf-8") as file:
            diff_content = file.read()

        global_changes = GlobalChanges()
        global_changes.parse_diff(diff_content)
        logger.logger.info("Parsing complete.")
        return global_changes

    except FileNotFoundError:
        logger.logger.error("File '{}' not found".format(diff_filename))
        sys.exit(1)
