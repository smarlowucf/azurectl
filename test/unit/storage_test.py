import sys
import mock
from nose.tools import *
from azure_cli.azure_account import AzureAccount
from azure_cli.azurectl_exceptions import *
from azure_cli.storage import Storage

import azure_cli


class TestStorage:
    def setup(self):
        account = AzureAccount('default', '../data/config')
        account.storage_names = mock.Mock(return_value=['a', 'b'])
        self.storage = Storage(account)

    def test_list(self):
        assert self.storage.list() == ['a', 'b']
