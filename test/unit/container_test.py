import datetime
import sys
import mock
from mock import patch
from nose.tools import *
from azure_cli.azurectl_exceptions import *
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
        account.storage_name = mock.Mock(return_value='mock-storage')
        account.storage_key = mock.Mock(
            return_value='fI8bhf6QAvgwCgR9qJyoNLHQ9F73fQ97e3/e8jMCFSiFioaB' +
            'iAU0oSGcFACtniSY6pS3L5GKNzPCK0FF6M+O4A=='
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

    def test_sas(self):
        container = 'mock-container'
        start = datetime.datetime(2015, 1, 1)
        expiry = datetime.datetime(2015, 12, 31)
        permissions = 'rl'
        assert self.container.sas(container, start, expiry, permissions) == \
            'https://mock-storage.blob.core.windows.net/mock-container?' + \
            'st=2015-01-01T00%3A00%3A00Z&se=2015-12-31T00%3A00%3A00Z&' + \
            'sp=rl&sr=c&sv=2012-02-12&' + \
            'sig=r48rEEchZ98nLO/HTc8RbrT4Sgw70NYrfooJRIJZG2Q%3D&'
