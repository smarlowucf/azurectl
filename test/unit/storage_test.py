import sys
import mock
from nose.tools import *
from azure_cli.storage_account import StorageAccount
from azure_cli.exceptions import *
from azure_cli.storage import Storage

import azure_cli

class TestStorage:
    def setup(self):
        account = StorageAccount('default', '../data/config')
        StorageAccount.list = mock.Mock(return_value=['a', 'b'])
        self.storage = Storage(account)

    def test_list(self):
        assert self.storage.list() == ['a', 'b']
