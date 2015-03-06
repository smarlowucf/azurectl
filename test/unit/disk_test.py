import sys
import mock
from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.disk import Disk

import azure_cli

from collections import namedtuple

class FakeBlobService:
    def delete_blob(self, container, blob):
        raise azure.WindowsAzureMissingResourceError("fake-raise")

class TestDisk:
    def setup(self):
        azure_cli.disk.XZ = mock.Mock(
            return_value=mock.Mock()
        )
        account = mock.Mock()
        self.disk = Disk(account, 'some-container')

    @raises(AzureDiskImageNotFound)
    def test_upload_disk_not_found(self):
        self.disk.upload('some-disk-image', None)

    @raises(AzureDiskUploadError)
    def test_upload(self):
        azure_cli.disk.BlobService = mock.Mock(
            return_value=FakeBlobService()
        )
        self.disk.upload('../data/config', None, 1024)

    @raises(AzureDiskDeleteError)
    def test_delete(self):
        self.disk.delete('some-blob')

    def test_print_upload_status(self):
        self.disk.print_upload_status()
        assert self.disk.upload_status == \
            {'current_bytes': 0, 'total_bytes': 0}
