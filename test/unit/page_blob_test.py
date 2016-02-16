import sys
import mock
from mock import patch
from mock import call
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.page_blob import PageBlob

import azurectl


class TestPageBlob:
    def setup(self):
        self.data_stream = mock.MagicMock()
        self.blob_service = mock.Mock()
        self.blob_service._BLOB_MAX_CHUNK_DATA_SIZE = 4096

        self.context_manager_mock = mock.Mock()
        self.file_mock = mock.Mock()
        self.enter_mock = mock.Mock()
        self.exit_mock = mock.Mock()
        self.enter_mock.return_value = self.file_mock
        setattr(self.context_manager_mock, '__enter__', self.enter_mock)
        setattr(self.context_manager_mock, '__exit__', self.exit_mock)

        self.page_blob = PageBlob(
            self.blob_service, 'blob-name', 'container-name', 1024
        )

        self.blob_service.put_blob.assert_called_once_with(
            'container-name', 'blob-name', None, 'PageBlob',
            None, None, None, None, None, None, None, None,
            None, None, None, 1024, None
        )

    def test_iterator(self):
        assert self.page_blob.__iter__() == self.page_blob

    @raises(AzurePageBlobSetupError)
    def test_put_blob_raises(self):
        self.blob_service.put_blob.side_effect = Exception
        PageBlob(self.blob_service, 'blob-name', 'container-name', 1024)

    @raises(AzurePageBlobAlignmentViolation)
    def test_page_alignment_invalid(self):
        PageBlob(self.blob_service, 'blob-name', 'container-name', 12)

    @raises(AzurePageBlobZeroPageError)
    @patch('__builtin__.open')
    def test_zero_page_read_failed(self, mock_open):
        mock_open.side_effect = Exception
        self.page_blob.next(self.data_stream)

    @patch('__builtin__.open')
    def test_zero_page_for_max_chunk_size(self, mock_open):
        self.page_blob.rest_bytes = self.blob_service._BLOB_MAX_CHUNK_DATA_SIZE
        mock_open.return_value = self.context_manager_mock
        self.page_blob.next(self.data_stream)
        self.file_mock.read.assert_called_once_with(
            self.blob_service._BLOB_MAX_CHUNK_DATA_SIZE
        )

    @patch('__builtin__.open')
    def test_zero_page_for_chunk(self, mock_open):
        self.page_blob.rest_bytes = 42
        mock_open.return_value = self.context_manager_mock
        self.page_blob.next(self.data_stream)
        self.file_mock.read.assert_called_once_with(42)

    def test_put_page(self):
        self.data_stream.read.return_value = 'some-data'
        self.page_blob.next(self.data_stream)
        self.blob_service.put_page.assert_called_once_with(
            'container-name', 'blob-name', 'some-data', 'bytes=0-8',
            'update', x_ms_lease_id=None
        )

    @raises(AzurePageBlobUpdateError)
    def test_put_page_max_retries_reached(self):
        self.blob_service.put_page.side_effect = Exception
        self.page_blob.next(self.data_stream)

    def test_put_page_retried_two_times(self):
        retries = [True, False, False]

        def side_effect(container, blob, data, location, update, x_ms_lease_id):
            if not retries.pop():
                raise Exception

        self.blob_service.put_page.side_effect = side_effect
        self.page_blob.next(self.data_stream)
        assert len(self.blob_service.put_page.call_args_list) == 3

    @raises(StopIteration)
    def test_next_page_update_no_data(self):
        self.data_stream.read.return_value = None
        self.page_blob.next(self.data_stream)
