import sys
import mock
from mock import patch
from mock import call
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
    @patch('os.path.exists')
    def test_upload_storage_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        self.storage.upload('some-blob', None)

    @raises(AzureStorageStreamError)
    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.XZ.open')
    def test_upload_error_stream_open(
        self, mock_xz_open, mock_uncompressed_size
    ):
        mock_uncompressed_size.return_value = 1024
        mock_xz_open.side_effect = Exception
        self.storage.upload('../data/blob.xz')

    @raises(AzureStorageUploadError)
    @patch('azurectl.storage.BlockBlobService.create_blob_from_stream')
    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.XZ.open')
    def test_upload_create_blob_from_stream_error(
        self, mock_xz_open, mock_uncompressed_size, mock_create_blob
    ):
        mock_uncompressed_size.return_value = 1024
        stream = mock.Mock
        stream.close = mock.Mock()
        mock_xz_open.return_value = stream
        mock_create_blob.side_effect = Exception
        self.storage.upload('../data/blob.xz')
        stream.close.assert_called_once_with()

    @raises(AzurePageBlobAlignmentViolation)
    def test_upload_alignment_error(self):
        self.storage.upload('../data/blob.xz')

    @patch('azurectl.storage.BlockBlobService')
    @patch('azurectl.storage.XZ.uncompressed_size')
    @patch('azurectl.storage.XZ.open')
    def test_upload(self, mock_xz_open, mock_uncompressed_size, mock_blob):
        blob_service = mock.Mock()
        blob_service.MAX_CHUNK_GET_SIZE = 1024
        mock_blob.return_value = blob_service
        stream = mock.Mock
        stream.close = mock.Mock()
        mock_xz_open.return_value = stream
        mock_uncompressed_size.return_value = 1024

        self.storage.upload(image='../data/blob.xz', max_chunk_size=512)
        blob_service.create_blob_from_stream.assert_called_once_with(
            blob_name='blob.xz',
            container_name='some-container',
            count=1024,
            max_retries=5,
            progress_callback=self.storage._Storage__upload_status,
            stream=stream
        )
        stream.close.assert_called_once_with()

    @patch('azurectl.storage.FileType')
    @patch('azurectl.storage.BlockBlobService')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    def test_upload_uncompressed(
        self, mock_open, mock_getsize, mock_blob, mock_file_type
    ):
        mock_getsize.return_value = 1024
        file_type = mock.Mock()
        file_type.is_xz = mock.Mock(
            return_value=False
        )
        mock_file_type.return_value = file_type
        blob_service = mock.Mock()
        blob_service.MAX_CHUNK_GET_SIZE = 1024
        mock_blob.return_value = blob_service
        stream = mock.Mock
        stream.close = mock.Mock()
        mock_open.return_value = stream

        self.storage.upload('../data/blob.xz')
        blob_service.create_blob_from_stream.assert_called_once_with(
            blob_name='blob.xz',
            container_name='some-container',
            count=1024,
            max_retries=5,
            progress_callback=self.storage._Storage__upload_status,
            stream=stream
        )
        stream.close.assert_called_once_with()

    @raises(AzureStorageDeleteError)
    def test_delete(self):
        self.storage.delete('some-blob')

    def test_print_upload_status(self):
        self.storage.print_upload_status()
        assert self.storage.upload_status == \
            {'current_bytes': 0, 'total_bytes': 0}

    def test_upload_status(self):
        self.storage._Storage__upload_status(50, 100)
        assert self.storage.upload_status == {
            'current_bytes': 50,
            'total_bytes': 100
        }
