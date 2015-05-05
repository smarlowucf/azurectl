import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azure_cli.azure_account import AzureAccount
from azure_cli.azurectl_exceptions import *
from azure_cli.image import Image

import azure_cli

from collections import namedtuple


class TestImage:
    def setup(self):
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

    @patch('azure_cli.image.ServiceManagementService.list_os_images')
    def test_list(self, mock_list_os_images):
        mock_list_os_images.return_value = self.list_os_images
        assert self.image.list() == [self.list_os_images.pop()._asdict()]

    @raises(AzureBlobServicePropertyError)
    def test_create_raise_blob_error(self):
        self.image.create('some-name', 'some-blob')

    @patch('azure_cli.image.BlobService.get_blob_properties')
    @raises(AzureOsImageCreateError)
    def test_create_raise_os_image_error(self, mock_get_blob_props):
        self.image.create('some-name', 'some-blob')

    @patch('azure_cli.image.ServiceManagementService.add_os_image')
    @patch('azure_cli.image.BlobService.get_blob_properties')
    def test_create(self, mock_get_blob_props, mock_add_os_image):
        MyStatus = namedtuple(
            'MyStatus',
            'status'
        )
        mock_status = mock.Mock()
        mock_status.get_operation_status = mock.Mock(
            return_value=MyStatus(status='OK')
        )
        mock_add_os_image.return_value = mock_status
        assert self.image.create(
            'some-name', 'some-blob', 'some-label'
        ) == 'OK'
        mock_add_os_image.assert_called_once_with(
            'some-label',
            'https://bob.blob.core.windows.net/foo/some-blob',
            'some-name',
            'Linux'
        )
