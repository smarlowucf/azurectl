import mock
from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.storage_account import StorageAccount

import azure_cli

class FakeStorageService:
    def storage_service_keys(self):
        MyStruct = namedtuple("MyStruct", "primary")
        return MyStruct(primary = 'foo')

class TestStorageAccount:
    def setup(self):
        self.storage = StorageAccount('default', '../data/config')
        azure_cli.storage_account.__query_service_account_for = mock.Mock(
            return_value=FakeStorageService()
        )

    def test_get_account_name(self):
        assert self.storage.get_account_name() == 'bob'

    def test_get_account_key(self):
        assert self.storage.get_account_key() == 'foo'
