# project
from exceptions import *

class Storage:
    def __init__(self, storage_account):
        self.account = storage_account

    def list(self):
        try:
            return self.account.list()
        except Exception as e:
            raise AzureStorageListError('%s (%s)' %(type(e), str(e)))
