import sys
import mock
from mock import patch


from test_helper import *

from azurectl.account.service import AzureAccount
from azurectl.config.parser import Config
from azurectl.azurectl_exceptions import *
from azurectl.instance.virtual_machine import VirtualMachine

from azure.servicemanagement import OSVirtualHardDisk

import azurectl

from collections import namedtuple


class TestVirtualMachine:
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
        account = AzureAccount(
            Config(
                region_name='East US 2', filename='../data/config'
            )
        )
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id', 'management_url']
        )
        account.publishsettings = mock.Mock(
            return_value=credentials(
                private_key='abc',
                certificate='abc',
                subscription_id='4711',
                management_url='test.url'
            )
        )
        account.get_blob_service_host_base = mock.Mock(
            return_value='test.url'
        )
        account.storage_key = mock.Mock()
        self.account = account
        self.vm = VirtualMachine(account)
        self.system_config = self.vm.create_linux_configuration(
            'some-user', 'some-host'
        )

    def test_create_network_configuration(self):
        endpoint = self.vm.create_network_endpoint('SSH', 22, 22, 'TCP')
        config = self.vm.create_network_configuration([endpoint])
        assert config.input_endpoints[0].name == 'SSH'

    def test_create_network_endpoint(self):
        endpoint = self.vm.create_network_endpoint('SSH', 22, 22, 'TCP')
        assert endpoint.name == 'SSH'

    def test_create_linux_configuration(self):
        config = self.vm.create_linux_configuration(
            'user', 'instance-name', True, 'password',
            'custom-data', 'fingerprint'
        )
        assert config.user_name == 'user'

    @patch('azurectl.instance.virtual_machine.OSVirtualHardDisk')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.create_virtual_machine_deployment')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_hosted_service_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_os_image')
    def test_create_instance(
        self, mock_os_image, mock_storage_properties,
        mock_service_properties, mock_vm_create, mock_os_disk
    ):
        storage_properties = mock.MagicMock()
        storage_properties.storage_service_properties.location = 'region'
        mock_storage_properties.return_value = storage_properties

        service_properties = mock.MagicMock()
        service_properties.hosted_service_properties.location = 'region'
        mock_service_properties.return_value = service_properties

        image_locations = mock.MagicMock()
        image_locations.location = 'region'
        mock_os_image.return_value = image_locations

        os_disk = OSVirtualHardDisk('foo', 'foo')
        mock_os_disk.return_value = os_disk
        endpoint = self.vm.create_network_endpoint('SSH', 22, 22, 'TCP')
        network_config = self.vm.create_network_configuration([endpoint])
        result = self.vm.create_instance(
            'cloud-service',
            'foo.vhd',
            self.system_config,
            network_config,
            'some-label',
            reserved_ip_name='test_reserved_ip_name'
        )
        mock_os_disk.assert_called_once_with(
            'foo.vhd',
            'https://bob.blob.test.url/foo/cloud-service_instance_some-host_image_foo.vhd'
        )
        mock_vm_create.assert_called_once_with(
            deployment_slot='production',
            role_size='Small',
            deployment_name='cloud-service',
            service_name='cloud-service',
            os_virtual_hard_disk=os_disk,
            label='some-label',
            system_config=self.system_config,
            reserved_ip_name='test_reserved_ip_name',
            role_name='cloud-service',
            network_config=network_config,
            provision_guest_agent=True
        )
        assert result['instance_name'] == 'some-host'

    @patch('azurectl.instance.virtual_machine.ServiceManagementService.create_virtual_machine_deployment')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_hosted_service_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_os_image')
    @raises(AzureVmCreateError)
    def test_create_instance_raise_vm_create_error(
        self, mock_os_image, mock_storage_properties, mock_service_properties,
        mock_vm_create
    ):
        storage_properties = mock.MagicMock()
        storage_properties.storage_service_properties.location = 'region'
        mock_storage_properties.return_value = storage_properties

        service_properties = mock.MagicMock()
        service_properties.hosted_service_properties.location = 'region'
        mock_service_properties.return_value = service_properties

        image_locations = mock.MagicMock()
        image_locations.location = 'region'
        mock_os_image.return_value = image_locations

        mock_vm_create.side_effect = AzureVmCreateError
        result = self.vm.create_instance(
            'cloud-service', 'foo.vhd', self.system_config
        )

    @patch('azurectl.instance.virtual_machine.ServiceManagementService.delete_deployment')
    def test_delete_instance(self, mock_delete_deployment):
        self.vm.delete_instance('cloud-service', 'foo')
        mock_delete_deployment.assert_called_once_with(
            'cloud-service', 'foo'
        )

    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_hosted_service_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_storage_account_properties')
    @raises(AzureStorageNotReachableByCloudServiceError)
    def test_create_instance_raise_storage_not_reachable_error(
        self, mock_storage_properties, mock_service_properties
    ):
        storage_properties = mock.MagicMock()
        storage_properties.storage_service_properties.location = 'regionA'
        mock_storage_properties.return_value = storage_properties

        service_properties = mock.MagicMock()
        service_properties.hosted_service_properties.location = 'regionB'
        mock_service_properties.return_value = service_properties

        result = self.vm.create_instance(
            'foo', 'some-region', 'foo.vhd', self.system_config
        )

    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_hosted_service_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.instance.virtual_machine.ServiceManagementService.get_os_image')
    @raises(AzureImageNotReachableByCloudServiceError)
    def test_create_instance_raise_image_not_reachable_error(
        self, mock_os_image, mock_storage_properties, mock_service_properties
    ):
        storage_properties = mock.MagicMock()
        storage_properties.storage_service_properties.location = 'regionA'
        mock_storage_properties.return_value = storage_properties

        service_properties = mock.MagicMock()
        service_properties.hosted_service_properties.location = 'regionA'
        mock_service_properties.return_value = service_properties

        image_locations = mock.MagicMock()
        image_locations.location = 'regionB'
        mock_os_image.return_value = image_locations

        result = self.vm.create_instance(
            'foo', 'some-region', 'foo.vhd', self.system_config
        )

    @patch('azurectl.instance.virtual_machine.ServiceManagementService.delete_deployment')
    @raises(AzureVmDeleteError)
    def test_delete_instance_raise_vm_delete_error(self, modk_delete):
        modk_delete.side_effect = AzureVmDeleteError
        self.vm.delete_instance('cloud-service', 'foo')
