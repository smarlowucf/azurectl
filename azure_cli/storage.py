# project
from exceptions import *


class Storage:
    def __init__(self, account):
        self.account = account

    def list(self):
        try:
            return self.account.storage_names()
        except Exception as e:
            raise AzureStorageListError('%s (%s)' % (type(e), str(e)))
