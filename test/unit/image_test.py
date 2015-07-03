import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azure_account import AzureAccount
from azurectl.azurectl_exceptions import *
from azurectl.image import Image

import azurectl

from collections import namedtuple


class TestImage:
    def setup(self):
        MyResult = namedtuple(
            'MyResult',
            'request_id'
        )
        self.myrequest = MyResult(request_id=42)
        MyStruct = namedtuple(
            'MyStruct',
            'name label os category description location \
             affinity_group media_link'
        )
        self.list_os_images = [MyStruct(
            name='some-name',
            label='bob',
            os='linux',
            category='cloud',
            description='nice',
            location='here',
            affinity_group='ok',
            media_link='url'
        )]
        account = AzureAccount('default', '../data/config')
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
        account.storage_key = mock.Mock()
        self.image = Image(account)

    @patch('azurectl.image.ServiceManagementService.list_os_images')
    def test_list(self, mock_list_os_images):
        mock_list_os_images.return_value = self.list_os_images
        assert self.image.list() == [self.list_os_images.pop()._asdict()]

    @raises(AzureOsImageListError)
    def test_list_raises_error(self):
        self.image.list()

    @raises(AzureBlobServicePropertyError)
    def test_create_raise_blob_error(self):
        self.image.create('some-name', 'some-blob')

    @patch('azurectl.image.BlobService.get_blob_properties')
    @raises(AzureOsImageCreateError)
    def test_create_raise_os_image_error(self, mock_get_blob_props):
        self.image.create('some-name', 'some-blob')

    @patch('azurectl.image.ServiceManagementService.add_os_image')
    @patch('azurectl.image.BlobService.get_blob_properties')
    def test_create(self, mock_get_blob_props, mock_add_os_image):
        mock_add_os_image.return_value = self.myrequest
        request_id = self.image.create(
            'some-name', 'some-blob'
        )
        assert request_id == 42
        mock_add_os_image.assert_called_once_with(
            'some-name',
            'https://bob.blob.core.windows.net/foo/some-blob',
            'some-name',
            'Linux'
        )

    @patch('azurectl.image.ServiceManagementService.delete_vm_image')
    def test_delete(self, mock_add_delete_image):
        mock_add_delete_image.return_value = self.myrequest
        request_id = self.image.delete(
            'some-name', False
        )
        assert request_id == 42
        mock_add_delete_image.assert_called_once_with(
            'some-name', False
        )

    @raises(AzureOsImageDeleteError)
    def test_delete_raise_os_delete_error(self):
        self.image.delete('some-name')
