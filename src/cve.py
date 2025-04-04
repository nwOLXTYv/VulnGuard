import json
from tools import logger


class Cve:

    def __init__(self, name, path):
        self.logger = logger.PrettyLogger("Cve")
        self.id = name
        self.db_path = path
        self.last_update = ""
        self.description = ""
        self.code = ""
        self.__get_data()

    def __get_data(self):
        file = open(self.db_path, "r")
        data = json.load(file)
        self.last_update = data['cveMetadata']['dateUpdated']
        self.description = data['containers']['cna']['descriptions'][0]['value']
        self.pretty_print()

    def pretty_print(self):
        print(f"CVE id : {self.id}")
        print(f"CVE database path : {self.db_path}")
        print(f"CVE last updated : {self.last_update}")
        print(f"CVE description : {self.description}")
        print(f"Vulnerable code : \n {self.code}")
