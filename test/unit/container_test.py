import datetime
import sys
import mock
from mock import patch
from nose.tools import *
from urlparse import urlparse

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.container import Container

import azurectl

from collections import namedtuple

MOCK_STORAGE_NAME = 'mock-storage'


class TestContainer:
    def setup(self):
        name = namedtuple("name", "name")
        self.name_list = [name(name="a"), name(name="b")]
        account = mock.Mock()
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        account.storage_name = mock.Mock(return_value=MOCK_STORAGE_NAME)
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

    @patch('azurectl.container.BlobService.list_containers')
    def test_list(self, mock_list_containers):
        mock_list_containers.return_value = self.name_list
        assert self.container.list() == ['a', 'b']

    @patch('azurectl.container.BlobService.list_blobs')
    def test_content(self, mock_list_blobs):
        mock_list_blobs.return_value = self.name_list
        assert self.container.content('some-container') == \
            {'some-container': ['a', 'b']}

    def test_sas(self):
        container = 'mock-container'
        start = datetime.datetime(2015, 1, 1)
        expiry = datetime.datetime(2015, 12, 31)
        permissions = 'rl'
        parsed = urlparse(
            self.container.sas(container, start, expiry, permissions)
        )
        print parsed
        assert parsed.scheme == 'https'
        assert parsed.netloc == MOCK_STORAGE_NAME + \
            '.blob.core.windows.net'
        assert parsed.path == '/' + container
        assert 'st=2015-01-01T00%3A00%3A00Z&' in parsed.query
        assert 'se=2015-12-31T00%3A00%3A00Z' in parsed.query
        assert 'sp=rl&' in parsed.query
        assert 'sr=c&' in parsed.query
        assert 'sig=' in parsed.query  # can't actively validate the signature
