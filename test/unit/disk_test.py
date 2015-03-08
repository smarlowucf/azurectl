import sys
import mock
from mock import patch
from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.disk import Disk

import azure_cli

from collections import namedtuple

class TestDisk:
    def setup(self):
        account = mock.Mock()
        credentials = namedtuple('credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        account.publishsettings = mock.Mock(
            return_value = credentials(
                private_key = 'abc',
                certificate = 'abc',
                subscription_id = '4711'
            )
        )
        self.disk = Disk(account, 'some-container')

    @raises(AzureDiskImageNotFound)
    def test_upload_disk_not_found(self):
        self.disk.upload('some-disk-image', None)

    @raises(AzureDiskUploadError)
    @patch('azure_cli.disk.XZ.uncompressed_size')
    def test_upload(self, mock_uncompressed_size):
        mock_uncompressed_size.return_value = 1024
        self.disk.upload('../data/config', None, 1024)

    @raises(AzureDiskDeleteError)
    def test_delete(self):
        self.disk.delete('some-blob')

    def test_print_upload_status(self):
        self.disk.print_upload_status()
        assert self.disk.upload_status == \
            {'current_bytes': 0, 'total_bytes': 0}
