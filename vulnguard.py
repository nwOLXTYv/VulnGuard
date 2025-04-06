from src.cve import Cve
from src.database import Database

from tools.logger import PrettyLogger


def vulnguard(cve_name):
    logger = PrettyLogger("Vulnguard")
    db = Database()
    path = db.search(cve_name)
    vuln = Cve(cve_name, path)
    print(vuln)
    logger.logger.info("Analyse finished")


if __name__ == '__main__':
    vulnguard("CVE-2024-29013")
