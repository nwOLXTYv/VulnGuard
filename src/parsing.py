import re
import sys
from logging import Logger


# Global class containing all changed files
class GlobalChanges:
    def __init__(self):
        self.files = []

    def parse_diff(self, diff_content):
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
        if current_file:
            self.files.append(current_file)
        file_name = self.extract_file_name(line)
        return FileChanges(file_name)

    def finalize_parsing(self, current_file, current_diff):
        if current_file:
            if current_diff:
                current_file.diffs.append(current_diff)
            self.files.append(current_file)

    @staticmethod
    def is_new_file(line):
        return line.startswith("diff --git")

    @staticmethod
    def extract_file_name(line):
        file_name_match = re.search(r'diff --git a/(.+?) b/', line)
        if file_name_match:
            return file_name_match.group(1)
        return None

# File class containing all functions changed within this specific file
# Delimiter begins with diff --git
class FileChanges:
    def __init__(self, name):
        self.name = name
        self.diffs = []

    def process_new_diff(self, current_diff):
        if current_diff:
            self.diffs.append(current_diff)
        return DiffChanges()

    @staticmethod
    def is_new_diff(line):
        # Check for the pattern @@ -{numbers},{numbers} +{numbers},{numbers} @@
        return bool(re.match(r'@@ -\d+,\d+ \+\d+,\d+ @@ +?', line))

# Diff class containing the diff content of a specific function
# Delimiter begins with @@ -{numbers},{numbers} +{numbers},{numbers} @@ prototype function
class DiffChanges:
    def __init__(self):
        self.value = ""

    def accumulate_content(self, line):
        self.value += line + "\n"


def parse(diff_filename):
    logger = Logger("Parsing")
    try:
        with open(diff_filename, 'r') as file:
            diff_content = file.read()

        global_changes = GlobalChanges()
        global_changes.parse_diff(diff_content)
        return global_changes

    except FileNotFoundError:
        logger.error("File '{}' not found".format(diff_filename))
        exit(1)
