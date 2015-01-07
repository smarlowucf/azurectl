from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.storage_account import StorageAccount

class TestStorageAccount:
    def setup(self):
        self.storage = StorageAccount('default', '../data/config')

    def test_get_account_name(self):
        assert self.storage.get_account_name() == 'bob'

    def test_get_account_key(self):
        assert self.storage.get_account_key() == 'foo'
