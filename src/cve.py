import json
from tools import logger


class Cve:

    def __init__(self, name, path):
        self.logger = logger.PrettyLogger("Cve")
        self.id = name
        self.db_path = path
        self.version = ""
        self.description = ""
        self.code = ""
        self.__get_data()

    def __get_data(self):
        file = open(self.db_path, "r")
        data = json.load(file)
        print(data)
        self.version = data['cveMetadata']['dateUpdated']
        print(self.version)
        # Todo : error on the next line, idk why
        self.description = data['containers']['cna']['descriptions']['value']
        print(self.description)
