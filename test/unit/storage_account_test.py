import mock
from nose.tools import *

from azure_cli.exceptions import *

import azure_cli

from azure_cli.storage_account import StorageAccount

from collections import namedtuple

class FakeServiceAccount:
    def get_private_key(self):
        return 'foo'

    def get_cert(self):
        return 'foo'

    def get_subscription_id(self):
        return 'foo'


class FakeStorageService:
    def get_storage_account_keys(self, account):
        MyPrimary = namedtuple('MyPrimary', 'primary')
        MyKeys = namedtuple('MyKeys', 'storage_service_keys')
        return MyKeys(storage_service_keys = MyPrimary(primary = 'foo'))

    def list_storage_accounts(self):
        result = []
        MyKeys = namedtuple('MyKeys', 'service_name')
        result.append(MyKeys(service_name = 'foo'))
        return result


class TestStorageAccount:
    def setup(self):
        MyStruct = namedtuple("MyStruct", "primary")
        self.storage = StorageAccount('default', '../data/config')
        azure_cli.storage_account.ServiceAccount = mock.Mock(
            return_value=FakeServiceAccount()
        )
        azure_cli.storage_account.ServiceManagementService = mock.Mock(
            return_value=FakeStorageService()
        )

    def test_get_name(self):
        assert self.storage.get_name() == 'bob'

    def test_get_key(self):
        assert self.storage.get_key() == 'foo'

    def test_list(self):
        assert self.storage.list() == ['foo']
