"""
usage: azure-cli container <command>

commands:
    list   list available containers
"""

from exceptions import *
from logger import Logger

from azure.storage import BlobService

class Container:
    def __init__(self, account):
        self.account_name = account.get_account_name()
        self.account_key  = account.get_account_key()

    def list(self):
        result = []
        blob_service = BlobService(self.account_name, self.account_key)
        for container in blob_service.list_containers():
            result.append(str(container.name))
        return result
