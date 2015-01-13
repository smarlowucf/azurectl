import sys
import mock
from nose.tools import *
from azure_cli.storage_account import StorageAccount
from azure_cli.exceptions import *
from azure_cli.disk import Disk

import azure_cli

from collections import namedtuple

class FakeBlobService:
    def put_block_blob_from_path(
        self, container_name, blob_name, file_path,
        content_encoding=None, content_language=None,
        content_md5=None, cache_control=None,
        x_ms_blob_content_type=None,
        x_ms_blob_content_encoding=None,
        x_ms_blob_content_language=None,
        x_ms_blob_content_md5=None,
        x_ms_blob_cache_control=None,
        x_ms_meta_name_values=None,
        x_ms_lease_id=None, progress_callback=None
    ):
        raise azure.WindowsAzureMissingResourceError("fake-raise")

    def delete_blob(self, container, blob):
        raise azure.WindowsAzureMissingResourceError("fake-raise")

class TestDisk:
    def setup(self):
        account = StorageAccount('default', '../data/config')
        self.disk = Disk(account, 'some-container')

    @raises(AzureDiskImageNotFound)
    def test_uppload_disk_not_found(self):
        self.disk.upload('some-disk-image')

    @raises(AzureDiskUploadError)
    def test_upload(self):
        azure_cli.disk.BlobService = mock.Mock(
            return_value=FakeBlobService()
        )
        self.disk.upload('../data/config')

    @raises(AzureDiskDeleteError)
    def test_delete(self):
        self.disk.delete('some-disk-image')

    def test_print_upload_status(self):
        self.disk.print_upload_status()
        assert self.disk.upload_status == \
            {'current_bytes': 0, 'total_bytes': 0}
