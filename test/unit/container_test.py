import sys
import mock
from nose.tools import *
from azure_cli.storage_account import StorageAccount
from azure_cli.exceptions import *
from azure_cli.container import Container

import azure_cli

from collections import namedtuple

class FakeBlobService:
    def list_containers(self):
        MyStruct = namedtuple("MyStruct", "name")
        return [MyStruct(name = "a"), MyStruct(name = "b")]

class TestContainer:
    def setup(self):
        account = StorageAccount('default', '../data/config')
        self.container = Container(account)

    def test_list(self):
        azure_cli.container.BlobService = mock.Mock(
            return_value=FakeBlobService()
        )
        assert self.container.list() == ['a', 'b']
