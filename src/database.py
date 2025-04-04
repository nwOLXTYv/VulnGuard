import re
import time
from tools import logger
from fnmatch import fnmatch
from os import (system, chdir, walk, path)
from datetime import (datetime, timedelta)


class Database:
    """
    A class to manage and search the cvelistV5 database.

    This class handles the updating and searching of CVE entries within the cvelistV5 database.
    """

    def __init__(self, delta=10):
        """
        Initialize the Database with a specified update interval.

        @param delta: The time interval in minutes after which the database should be updated.
        """
        self.logger = logger.PrettyLogger("Database")
        self.path = "../cvelistV5/"
        self.update_delta = delta
        self.last_update = None
        self.__update()

    def __check_cve_regexp(self, cve):
        """
        Check if the CVE name matches the expected pattern.

        This method uses a regular expression to validate the format of the CVE name.

        @param cve: The CVE name to validate.
        @return: True if the CVE name matches the pattern, False otherwise.
        """
        pattern = re.compile(r"^CVE-\d{4}-\d{4,7}")
        match = pattern.match(cve)
        if match:
            self.logger.logger.info("CVE name matches regexp.")
        else:
            self.logger.logger.error("CVE name doesn't match regexp.")
        return match is not None

    def __update(self):
        """
        Update the cvelistV5 database by pulling the latest changes from the repository.

        This method changes the directory to the database path and performs a git pull to update the database.
        """
        chdir(self.path)
        self.logger.logger.info("Database update ...")
        start = time.process_time()
        system("git pull 1> /dev/null")
        self.last_update = datetime.now()
        end = time.process_time()
        self.logger.logger.info("Database update took %f seconds.", (end - start))

    def search(self, cve):
        """
        Search for a CVE entry in the cvelistV5 database.

        This method first checks if the CVE name is valid and updates the database if necessary.
        It then searches for the CVE entry in the database and returns the path if found.

        @param cve: The CVE name to search for.
        @return: The path to the CVE file if found, None otherwise.
        """
        if not self.__check_cve_regexp(cve):
            self.logger.logger.error("%s is not a valid CVE.", cve)
            exit(1)
        if self.last_update + timedelta(minutes=self.update_delta) < datetime.now():
            self.__update()
        for root, dirs, files in walk(self.path):
            for name in files:
                if fnmatch(name, cve + ".json"):
                    cve_path = path.join(root, name)
                    self.logger.logger.info("Found %s at %s", cve, cve_path)
                    return cve_path
        self.logger.logger.error("Could not find any %s.", cve)
        exit(1)
