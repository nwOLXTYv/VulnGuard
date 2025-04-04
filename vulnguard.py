import cve
import database

from logging import Logger


def vulnguard(cve_name):
    logger = Logger("Vulnguard")
    db = database.Database()
    path = db.search(cve_name)
    vuln = cve.Cve(cve_name, path)
    print(vuln)


if __name__ == '__main__':
    vulnguard("CVE-2024-29013")
