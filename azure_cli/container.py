"""
usage: azure-cli container list
       azure-cli container content <name>

commands:
    list     list available containers
    content  list content of given container
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
        try:
            for container in blob_service.list_containers():
                result.append(str(container.name))
        except Exception as e:
            raise AzureContainerListError('%s (%s)' %(type(e), str(e)))
        return result

    def content(self, container):
        result = {container: []}
        blob_service = BlobService(self.account_name, self.account_key)
        try:
            for blob in blob_service.list_blobs(container):
                result[container].append(str(blob.name))
            return result
        except Exception as e:
            raise AzureContainerListContentError('%s (%s)' %(type(e), str(e)))
