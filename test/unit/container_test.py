import sys
import mock
from mock import patch
from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.container import Container

import azure_cli

from collections import namedtuple


class TestContainer:
    def setup(self):
        name = namedtuple("name", "name")
        self.name_list = [name(name="a"), name(name="b")]
        account = mock.Mock()
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        account.publishsettings = mock.Mock(
            return_value=credentials(
                private_key='abc',
                certificate='abc',
                subscription_id='4711'
            )
        )
        self.container = Container(account)

    @patch('azure_cli.container.BlobService.list_containers')
    def test_list(self, mock_list_containers):
        mock_list_containers.return_value = self.name_list
        assert self.container.list() == ['a', 'b']

    @patch('azure_cli.container.BlobService.list_blobs')
    def test_content(self, mock_list_blobs):
        mock_list_blobs.return_value = self.name_list
        assert self.container.content('some-container') == \
            {'some-container': ['a', 'b']}
