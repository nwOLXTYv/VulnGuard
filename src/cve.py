"""
@file Cve.py
@brief Contains all cve function and classes
"""

import json
from tools.logger import PrettyLogger


class Cve:
    """
    @class Cve
    @brief Represents a Common Vulnerabilities and Exposures (CVE) entry.

    This class encapsulates information about a CVE, including its ID, database path,
    last update date, description, and vulnerable code. It reads data from a JSON file
    and provides a method to print the CVE details in a formatted manner.
    """

    def __init__(self, name, path):
        """
        @brief Constructs a new Cve object.

        @param name The ID of the CVE.
        @param path The file path to the CVE database.
        """
        self.logger = PrettyLogger("Cve")
        self.id = name
        self.db_path = path
        self.last_update = ""
        self.description = ""
        self.code = ""
        self.__get_data()

    def __get_data(self):
        """
        @brief Private method to load CVE data from a JSON file.

        This method reads the CVE data from the specified file path and populates
        the object's attributes with the relevant information.
        """
        file = open(self.db_path, "r")
        data = json.load(file)
        try:
            self.last_update = data['cveMetadata']['dateUpdated']
            self.description = data['containers']['cna']['descriptions'][0]['value']
            self.logger.logger.info("Successfully loaded CVE data from '{}'".format(self.db_path))
        except Exception as e:
            self.logger.logger.error("Failed to load CVE data from '{}'".format(self.db_path))
            self.logger.logger.error(e)
            exit(1)
        self.pretty_print()

    def pretty_print(self):
        """
        @brief Prints the CVE details in a formatted manner.

        This method outputs the CVE ID, database path, last update date, description,
        and vulnerable code to the console.
        """
        print(f"CVE id : {self.id}")
        print(f"CVE database path : {self.db_path}")
        print(f"CVE last updated : {self.last_update}")
        print(f"CVE description : {self.description}")
        print(f"Vulnerable code : \n {self.code}")
