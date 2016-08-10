import sys
import mock
import random
from azure.common import AzureMissingResourceHttpError
from collections import namedtuple
from datetime import datetime
from mock import patch
from test_helper import *

from azurectl.account.service import AzureAccount
from azurectl.azurectl_exceptions import *
from azurectl.config.parser import Config
from azurectl.instance.data_disk import DataDisk

from collections import namedtuple

import azurectl


class TestDataDisk:
    def setup(self):
        # construct an account
        account = AzureAccount(
            Config(
                region_name='East US 2', filename='../data/config'
            )
        )
        self.service = mock.Mock()
        account.get_management_service = mock.Mock(return_value=self.service)
        account.get_blob_service_host_base = mock.Mock(
            return_value='test.url'
        )
        account.storage_key = mock.Mock()
        # now that that's done, instantiate a DataDisk with the account
        self.data_disk = DataDisk(account)
        # asynchronous API operations return a request object
        self.my_request = mock.Mock(request_id=42)
        # variables used in multiple tests
        self.cloud_service_name = 'mockcloudservice'
        self.instance_name = 'mockcloudserviceinstance1'
        self.lun = 0
        self.host_caching = 'ReadWrite'
        self.disk_filename = 'mockcloudserviceinstance1-data-disk-0.vhd'
        self.disk_name = 'mockcloudserviceinstance1-data-disk-0'
        self.disk_url = (
            'https://' +
            account.storage_name() +
            '.blob.' +
            account.get_blob_service_host_base() + '/' +
            account.storage_container() + '/' +
            self.disk_filename
        )
        self.disk_label = 'Mock data disk'
        self.disk_size = 42
        self.timestamp = datetime.utcnow()
        self.time_string = datetime.isoformat(self.timestamp).replace(':', '_')
        self.account = account

    @raises(AzureDataDiskCreateError)
    def test_create_error(self):
        # given
        self.service.add_data_disk.side_effect = Exception
        # when
        self.data_disk.create(
            size=self.disk_size,
            cloud_service_name=self.cloud_service_name,
            instance_name=None,
            lun=self.lun,
            host_caching=self.host_caching,
            filename=self.disk_filename,
            label=self.disk_label
        )

    @raises(AzureDataDiskDeleteError)
    def test_delete_error(self):
        # given
        self.service.delete_disk.side_effect = Exception
        # when
        self.data_disk.delete(self.disk_name)

    @raises(AzureDataDiskDeleteError)
    def test_detach_error(self):
        # given
        self.service.delete_data_disk.side_effect = Exception
        # when
        self.data_disk.detach(self.lun, self.cloud_service_name)

    @raises(AzureDataDiskShowError)
    def test_show_attached_error(self):
        # given
        self.service.get_data_disk.side_effect = Exception
        # when
        self.data_disk.show_attached(
            self.cloud_service_name, self.instance_name, self.lun
        )

    def test_show_attached_no_raise_for_all_lun_list(self):
        # given
        self.service.get_data_disk.side_effect = Exception
        # when
        result = self.data_disk.show_attached(
            self.cloud_service_name
        )
        assert result == []

    @raises(AzureDataDiskShowError)
    def test_show_error(self):
        # given
        self.service.get_disk.side_effect = Exception
        # when
        self.data_disk.show(self.disk_name)

    @raises(AzureDataDiskNoAvailableLun)
    def test_no_available_lun_exception(self):
        # given
        self.service.get_data_disk.side_effect = iter([
            self.__create_mock_data_disk(i) for i in range(16)
        ])
        # when
        self.data_disk._DataDisk__get_first_available_lun(
            self.cloud_service_name, self.instance_name
        )
        # then
        assert self.service.get_data_disk.call_count == 16

    @patch('azurectl.instance.data_disk.datetime')
    def test_generate_filename(self, mock_timestamp):
        # given
        mock_timestamp.utcnow = mock.Mock(return_value=self.timestamp)
        mock_timestamp.isoformat = mock.Mock(return_value=self.time_string)
        expected = '%s-data-disk-%s.vhd' % (
            self.instance_name,
            self.time_string
        )
        # when
        result = self.data_disk._DataDisk__generate_filename(
            identifier=self.instance_name
        )
        # then
        assert result == expected

    def test_get_first_available_lun(self):
        # given
        self.service.get_data_disk.side_effect = iter([
            self.__create_mock_data_disk(0),
            self.__create_mock_data_disk(1),
            AzureMissingResourceHttpError('NOT FOUND', 404)
        ])
        # when
        result = self.data_disk._DataDisk__get_first_available_lun(
            self.cloud_service_name, self.instance_name
        )
        # then
        assert self.service.get_data_disk.call_count == 3
        assert result == 2  # 0 and 1 are taken

    def test_create(self):
        # given
        self.service.add_data_disk.return_value = self.my_request
        # when
        result = self.data_disk.create(
            self.disk_size,
            lun=self.lun,
            cloud_service_name=self.cloud_service_name,
            instance_name=None,
            host_caching=self.host_caching,
            filename=self.disk_filename,
            label=self.disk_label
        )
        # then
        assert result == self.my_request.request_id
        self.service.add_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.cloud_service_name,
            self.lun,
            host_caching=self.host_caching,
            media_link=self.disk_url,
            disk_label=self.disk_label,
            logical_disk_size_in_gb=self.disk_size
        )

    @patch('azurectl.instance.data_disk.DataDisk._DataDisk__get_first_available_lun')
    def test_create_without_lun(self, mock_lun):
        # given
        self.service.add_data_disk.return_value = self.my_request
        mock_lun.return_value = 0
        # when
        result = self.data_disk.create(
            self.disk_size,
            cloud_service_name=self.cloud_service_name,
            instance_name=self.instance_name,
            lun=None,
            host_caching=self.host_caching,
            filename=self.disk_filename,
            label=self.disk_label
        )
        # then
        self.service.add_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.instance_name,
            0,
            host_caching=self.host_caching,
            media_link=self.disk_url,
            disk_label=self.disk_label,
            logical_disk_size_in_gb=self.disk_size
        )

    def test_show(self):
        # given
        self.service.get_disk.return_value = self.__create_mock_disk()
        expected = self.__create_expected_disk_output()
        # when
        result = self.data_disk.show(self.disk_name)
        # then
        self.service.get_disk.assert_called_once_with(
            self.disk_name
        )
        assert result == expected

    def test_show_attached(self):
        # given
        self.service.get_data_disk.return_value = self.__create_mock_data_disk(
            self.lun
        )
        expected = self.__create_expected_data_disk_output(self.lun)
        # when
        result = self.data_disk.show_attached(
            self.cloud_service_name, self.instance_name, self.lun
        )
        # then
        self.service.get_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.instance_name,
            self.lun
        )
        assert result == expected

    def test_list(self):
        # given
        self.service.list_disks.return_value = [self.__create_mock_disk()]
        expected = self.__create_expected_disk_list_output()
        # when
        result = self.data_disk.list()
        # then
        self.service.list_disks.assert_called_once_with()
        assert result == expected

    def test_list_empty(self):
        # given
        self.service.list_disks.side_effect = Exception
        # when
        result = self.data_disk.list()
        # then
        self.service.list_disks.assert_called_once_with()
        assert result == []

    def test_detach(self):
        # given
        self.service.delete_data_disk.return_value = self.my_request
        # when
        result = self.data_disk.detach(
            self.lun, self.cloud_service_name, self.instance_name
        )
        # then
        self.service.delete_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.instance_name,
            self.lun,
            delete_vhd=False
        )
        assert result == self.my_request.request_id

    def test_detach_no_instance_name(self):
        # given
        self.service.delete_data_disk.return_value = self.my_request
        # when
        result = self.data_disk.detach(
            self.lun, self.cloud_service_name
        )
        # then
        self.service.delete_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.cloud_service_name,
            self.lun,
            delete_vhd=False
        )
        assert result == self.my_request.request_id

    def test_delete(self):
        # given
        self.service.delete_disk.return_value = self.my_request
        # when
        result = self.data_disk.delete(self.disk_name)
        # then
        self.service.delete_disk.assert_called_once_with(
            self.disk_name, delete_vhd=True
        )

    def __create_mock_data_disk(self, lun):
        data_disk_type = namedtuple(
            'data_disk_type', [
                'host_caching', 'disk_label', 'disk_name', 'lun',
                'logical_disk_size_in_gb', 'media_link', 'source_media_link'
            ]
        )
        return data_disk_type(
            host_caching=self.host_caching,
            disk_label=self.disk_label,
            disk_name=self.disk_name,
            lun=lun,
            logical_disk_size_in_gb=self.disk_size,
            media_link=self.disk_url,
            source_media_link=''
        )

    def __create_mock_disk(self):
        disk_type = namedtuple(
            'disk_type', [
                'affinity_group', 'attached_to', 'has_operating_system',
                'is_corrupted', 'location', 'logical_disk_size_in_gb',
                'label', 'media_link', 'name', 'os', 'source_image_name'
            ]
        )
        attach_info_type = namedtuple(
            'attach_info_type', [
                'hosted_service_name', 'deployment_name', 'role_name'
            ]
        )
        return disk_type(
            affinity_group='',
            attached_to=attach_info_type(
                hosted_service_name='',
                deployment_name='',
                role_name=''
            ),
            has_operating_system=False,
            is_corrupted=False,
            location='',
            logical_disk_size_in_gb=self.disk_size,
            label=self.disk_label,
            media_link=self.disk_url,
            name=self.disk_name,
            os='Linux',
            source_image_name=''
        )

    def __create_expected_data_disk_output(self, lun):
        return [
            {
                'size': '%d GB' % self.disk_size,
                'label': self.disk_label,
                'disk-url': self.disk_url,
                'source-image-url': '',
                'lun': lun,
                'host-caching': 'ReadWrite'
            }
        ]

    def __create_expected_disk_output(self):
        return {
            'affinity_group': '',
            'attached_to': {
                'hosted_service_name': '',
                'deployment_name': '',
                'role_name': ''
            },
            'has_operating_system': False,
            'is_corrupted': False,
            'location': '',
            'logical_disk_size_in_gb': '%d GB' % self.disk_size,
            'label': self.disk_label,
            'media_link': self.disk_url,
            'name': self.disk_name,
            'os': 'Linux',
            'source_image_name': ''
        }

    def __create_expected_disk_list_output(self):
        return [
            {
                'is_attached': True,
                'name': self.disk_name
            }
        ]
