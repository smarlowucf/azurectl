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
            self.lun, self.cloud_service_name
        )

    @raises(AzureDataDiskShowError)
    def test_show_error(self):
        # given
        self.service.get_disk.side_effect = Exception
        # when
        self.data_disk.show(self.disk_name)

    @raises(AzureDataDiskCreateError)
    def test_attach_error(self):
        # given
        self.service.add_data_disk.side_effect = Exception
        # when
        self.data_disk.attach(
            self.disk_name,
            self.cloud_service_name,
            self.instance_name,
            self.disk_label,
            self.lun,
            self.host_caching
        )

    @raises(AzureDataDiskCreateError)
    @patch('azurectl.instance.data_disk.subprocess.Popen')
    def test_create_error_on_qemu_img(self, mock_popen):
        # given
        vhd_image = mock.Mock()
        vhd_image.communicate = mock.MagicMock(
            return_value = ['output', 'error']
        )
        vhd_image.returncode = 1
        mock_popen.return_value = vhd_image
        # when
        self.data_disk.create(
            identifier=self.instance_name, disk_size_in_gb=20
        )

    @raises(AzureDataDiskCreateError)
    @patch('azurectl.instance.data_disk.subprocess.Popen')
    @patch('azurectl.instance.data_disk.Storage')
    def test_create_error_on_vhd_upload(self, mock_storage, mock_popen):
        # given
        vhd_image = mock.MagicMock()
        vhd_image.communicate = mock.MagicMock(
            return_value = ['output', 'error']
        )
        vhd_image.returncode = 0
        mock_popen.return_value = vhd_image
        mock_storage.side_effect = Exception
        # when
        self.data_disk.create(
            identifier=self.instance_name, disk_size_in_gb=20
        )

    @raises(AzureDataDiskCreateError)
    @patch('azurectl.instance.data_disk.subprocess.Popen')
    @patch('azurectl.instance.data_disk.Storage')
    def test_create_error_on_add_disk(self, mock_storage, mock_popen):
        # given
        vhd_image = mock.MagicMock()
        vhd_image.communicate = mock.MagicMock(
            return_value = ['output', 'error']
        )
        vhd_image.returncode = 0
        mock_popen.return_value = vhd_image
        self.service.add_disk.side_effect = Exception
        # when
        self.data_disk.create(
            identifier=self.instance_name, disk_size_in_gb=20
        )

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

    @patch('azurectl.instance.data_disk.datetime')
    @patch('azurectl.instance.data_disk.subprocess.Popen')
    @patch('azurectl.instance.data_disk.Storage')
    @patch('azurectl.instance.data_disk.NamedTemporaryFile')
    def test_create(self, mock_tmp, mock_storage, mock_popen, mock_datetime):
        # given
        tmpfile = mock.Mock()
        tmpfile.name = 'tmpfile'
        mock_tmp.return_value = tmpfile
        vhd_image = mock.MagicMock()
        vhd_image.communicate = mock.MagicMock(
            return_value = ['output', 'error']
        )
        vhd_image.returncode = 0
        mock_popen.return_value = vhd_image
        self.service.add_disk.return_value = self.my_request
        mock_datetime.isoformat.return_value = '0'
        # when
        result = self.data_disk.create(
            identifier=self.instance_name,
            disk_size_in_gb=20,
            label=self.disk_label
        )
        # then
        mock_popen.assert_called_once_with(
            [
                'qemu-img', 'create', '-f', 'vpc', '-o',
                'subformat=fixed,size=20G,force_size=on', 'tmpfile'
            ], stderr=-1, stdout=-1
        )
        mock_storage.assert_called_once_with(
            self.account, self.account.storage_container()
        )
        self.service.add_disk.assert_called_once_with(
            media_link=self.disk_url,
            name=self.data_disk.data_disk_name.replace('.vhd', ''),
            label=self.disk_label,
            has_operating_system=False,
            os='Linux',
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
            self.lun, self.cloud_service_name, self.instance_name
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

    def test_list_attached(self):
        # given
        number_of_disks = random.randint(0, 15)
        luns = random.sample(range(16), number_of_disks)
        luns.sort()
        mock_disk_set = [AzureMissingResourceHttpError('NOT FOUND', 404)] * 16
        expected_result = []
        for lun in luns:
            mock_disk_set[lun] = self.__create_mock_data_disk(lun)
            expected_result.append(self.__create_expected_data_disk_output(lun))
        self.service.get_data_disk.side_effect = iter(mock_disk_set)
        # when
        result = self.data_disk.list_attached(
            self.cloud_service_name
        )
        # then
        assert result == expected_result

    def test_attach(self):
        # given
        self.service.add_data_disk.return_value = self.my_request
        # when
        result = self.data_disk.attach(
            self.disk_name,
            self.cloud_service_name,
            self.instance_name,
            self.disk_label,
            self.lun,
            self.host_caching
        )
        # then
        assert result == self.my_request.request_id
        self.service.add_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.instance_name,
            self.lun,
            host_caching=self.host_caching,
            media_link=self.disk_url,
            disk_label=self.disk_label,
            disk_name=self.disk_name
        )

    @patch('azurectl.instance.data_disk.datetime')
    def test_attach_without_lun(self, mock_datetime):
        # given
        # mock no data disks attached has to result in lun 0 assigned later
        self.service.get_data_disk.side_effect = AzureMissingResourceHttpError(
            'NOT FOUND', 404
        )
        mock_datetime.isoformat.return_value = '0'
        self.service.add_data_disk.return_value = self.my_request
        # when
        result = self.data_disk.attach(
            self.disk_name,
            self.cloud_service_name
        )
        # then
        self.service.add_data_disk.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.cloud_service_name,
            0,
            media_link=self.disk_url,
            disk_name=self.disk_name
        )

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
        return {
            'size': '%d GB' % self.disk_size,
            'label': self.disk_label,
            'disk-url': self.disk_url,
            'source-image-url': '',
            'lun': lun,
            'host-caching': 'ReadWrite'
        }

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
