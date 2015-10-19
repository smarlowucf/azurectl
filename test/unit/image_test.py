import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azure_account import AzureAccount
from azurectl.config import Config
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
            'affinity_group category description eula icon_uri image_family \
             is_premium label language location logical_size_in_gb media_link \
             name os os_state pricing_detail_link privacy_uri \
             published_date publisher_name recommended_vm_size show_in_gui \
             small_icon_uri'
        )
        self.list_os_images = [MyStruct(
            affinity_group='group',
            category='cloud',
            description='nice',
            eula='eula',
            icon_uri='url',
            image_family='disks',
            is_premium=False,
            label='bob',
            language='English',
            location='West US',
            logical_size_in_gb=30,
            media_link='url',
            name='some-name',
            os='linux',
            os_state='brilliant',
            pricing_detail_link='url',
            privacy_uri='url',
            published_date='date',
            publisher_name='suse',
            recommended_vm_size=10,
            show_in_gui=True,
            small_icon_uri='url'
        )]
        account = AzureAccount(
            Config(
                region_name='East US 2', filename='../data/config'
            )
        )
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

    @patch('azurectl.image.ServiceManagementService.list_os_images')
    @raises(AzureOsImageListError)
    def test_list_raises_error(self, mock_list_os_images):
        mock_list_os_images.side_effect = Exception
        self.image.list()

    @raises(AzureBlobServicePropertyError)
    def test_create_raise_blob_error(self):
        self.image.create('some-name', 'some-blob')

    @patch('azurectl.image.ServiceManagementService.add_os_image')
    @patch('azurectl.image.BlobService.get_blob_properties')
    @raises(AzureOsImageCreateError)
    def test_create_raise_os_image_error(self, mock_get_blob_props, mock_add_os_image):
        mock_add_os_image.side_effect = Exception
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

    @patch('azurectl.image.ServiceManagementService.delete_os_image')
    def test_delete(self, mock_delete_image):
        mock_delete_image.return_value = self.myrequest
        request_id = self.image.delete(
            'some-name', False
        )
        assert request_id == 42
        mock_delete_image.assert_called_once_with(
            'some-name', False
        )

    @patch('azurectl.image.ServiceManagementService.delete_os_image')
    @raises(AzureOsImageDeleteError)
    def test_delete_raise_os_delete_error(self, mock_delete_image):
        mock_delete_image.side_effect = Exception
        self.image.delete('some-name')

    @patch('azurectl.image.ComputeManagementService.replicate')
    def test_replicate(self, mock_replicate):
        mock_replicate.return_value = self.myrequest
        request_id = self.image.replicate(
            'some-name', ['a', 'b', 'c'], 'offer', 'sku', 'version'
        )
        assert request_id == 42
        mock_replicate.assert_called_once_with(
            'some-name', ['a', 'b', 'c'], 'offer', 'sku', 'version'
        )

    @patch('azurectl.image.ComputeManagementService.unreplicate')
    def test_unreplicate(self, mock_unreplicate):
        mock_unreplicate.return_value = self.myrequest
        request_id = self.image.unreplicate('some-name')
        assert request_id == 42
        mock_unreplicate.assert_called_once_with(
            'some-name'
        )

    @patch('azurectl.image.ComputeManagementService.share')
    def test_publish(self, mock_publish):
        mock_publish.return_value = self.myrequest
        request_id = self.image.publish('some-name', 'public')
        assert request_id == 42
        mock_publish.assert_called_once_with(
            'some-name', 'public'
        )

    @raises(AzureOsImageReplicateError)
    @patch('azurectl.image.ComputeManagementService.replicate')
    def test_replicate_raises_error(self, mock_replicate):
        mock_replicate.side_effect = AzureOsImageReplicateError
        self.image.replicate(
            'some-name', 'some-regions', 'offer', 'sku', 'version'
        )

    @raises(AzureOsImageUnReplicateError)
    @patch('azurectl.image.ComputeManagementService.unreplicate')
    def test_unreplicate_raises_error(self, mock_unreplicate):
        mock_unreplicate.side_effect = AzureOsImageUnReplicateError
        self.image.unreplicate('some-name')

    @raises(AzureOsImagePublishError)
    @patch('azurectl.image.ComputeManagementService.share')
    def test_publish_raises_error(self, mock_publish):
        mock_publish.side_effect = AzureOsImagePublishError
        self.image.publish('some-name', 'public')
