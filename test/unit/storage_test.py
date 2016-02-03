import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.storage import Storage

import azurectl

from collections import namedtuple


class TestStorage:
    def setup(self):
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
        self.storage = Storage(account, 'some-container')

    @raises(AzureStorageFileNotFound)
    def test_upload_storage_file_not_found(self):
        self.storage.upload('some-blob', None)

    @raises(AzureStorageUploadError)
    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.BlobService.put_blob')
    def test_upload_error_put_blob(self, put_blob, mock_uncompressed_size):
        mock_uncompressed_size.return_value = 1024
        self.storage.upload('../data/blob.xz', None, 1024)

    @raises(AzureStorageUploadError)
    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.BlobService.put_page')
    def test_upload_error_put_page(self, put_page, mock_uncompressed_size):
        mock_uncompressed_size.return_value = 1024
        self.storage.upload('../data/blob.xz', None, 1024, max_attempts=1)

    @raises(AzurePageBlobAlignmentViolation)
    @patch('azurectl.storage.XZ.uncompressed_size')
    def test_upload_alignment_error(self, mock_uncompressed_size):
        mock_uncompressed_size.return_value = 42
        self.storage.upload('../data/blob.xz', None)

    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.BlobService.put_blob')
    @patch('azurectl.storage.BlobService.put_page')
    def test_upload(self, put_page, put_blob, mock_uncompressed_size):
        mock_uncompressed_size.return_value = 1024
        self.storage.upload('../data/blob.xz', None)
        put_blob.assert_called_once_with(
            'some-container',
            'blob.xz',
            None,
            'PageBlob',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            1024,
            None
        )
        put_page.assert_called_once_with(
            'some-container',
            'blob.xz',
            'foo',
            'bytes=0-2',
            'update',
            x_ms_lease_id=None
        )

    @patch('azurectl.storage.BlobService.put_blob')
    @patch('azurectl.storage.BlobService.put_page')
    def test_upload_uncompressed(self, put_page, put_blob):
        self.storage.upload('../data/blob.raw', None)
        put_blob.assert_called_once_with(
            'some-container',
            'blob.raw',
            None,
            'PageBlob',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            1024,
            None
        )
        put_page.assert_called_once_with(
            'some-container',
            'blob.raw',
            mock.ANY,
            'bytes=0-1023',
            'update',
            x_ms_lease_id=None
        )

    @raises(AzureStorageDeleteError)
    def test_delete(self):
        self.storage.delete('some-blob')

    def test_print_upload_status(self):
        self.storage.print_upload_status()
        assert self.storage.upload_status == \
            {'current_bytes': 0, 'total_bytes': 0}
