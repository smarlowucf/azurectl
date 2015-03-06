import sys
import mock
from mock import patch
from nose.tools import *
from azure_cli.storage_account import StorageAccount
from azure_cli.exceptions import *
from azure_cli.container import Container

import azure_cli

from collections import namedtuple

class TestContainer:
    def setup(self):
        MyStruct = namedtuple("MyStruct", "name")
        self.list_blobs = [MyStruct(name = "a"), MyStruct(name = "b")]
        self.list_containers = [MyStruct(name = "a"), MyStruct(name = "b")]

        account = StorageAccount('default', '../data/config')
        StorageAccount.get_key = mock.Mock(return_value='foo')
        self.container = Container(account)

    @patch('azure_cli.container.BlobService.list_containers')
    def test_list(self, mock_list_containers):
        mock_list_containers.return_value = self.list_containers
        assert self.container.list() == ['a', 'b']

    @patch('azure_cli.container.BlobService.list_blobs')
    def test_content(self, mock_list_blobs):
        mock_list_blobs.return_value = self.list_blobs
        assert self.container.content('some-container') == \
            {'some-container': ['a', 'b']}
