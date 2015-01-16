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

    def list_blobs(self, container):
        MyStruct = namedtuple("MyStruct", "name")
        return [MyStruct(name = "a"), MyStruct(name = "b")]


class TestContainer:
    def setup(self):
        account = StorageAccount('default', '../data/config')
        StorageAccount.get_account_key = mock.Mock(return_value='foo')
        self.container = Container(account)

    def test_list(self):
        azure_cli.container.BlobService = mock.Mock(
            return_value=FakeBlobService()
        )
        assert self.container.list() == ['a', 'b']

    def test_content(self):
        azure_cli.container.BlobService = mock.Mock(
            return_value=FakeBlobService()
        )
        assert self.container.content('some-container') == \
            {'some-container': ['a', 'b']}
