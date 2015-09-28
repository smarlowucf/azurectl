import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azure_account import AzureAccount
from azurectl.config import Config
from azurectl.azurectl_exceptions import *
from azurectl.virtual_machine import VirtualMachine

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
            Config('bob', '../data/config')
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
        self.account = account
        self.vm = VirtualMachine(account)

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

    @patch('azurectl.virtual_machine.OSVirtualHardDisk')
    @patch('azurectl.virtual_machine.ServiceManagementService.create_virtual_machine_deployment')
    def test_create_instance(self, mock_vm_create, mock_os_disk):
        os_disk = OSVirtualHardDisk('foo', 'foo')
        mock_os_disk.return_value = os_disk
        system_config = self.vm.create_linux_configuration(
            'some-user', 'some-host'
        )
        endpoint = self.vm.create_network_endpoint('SSH', 22, 22, 'TCP')
        network_config = self.vm.create_network_configuration([endpoint])
        result = self.vm.create_instance(
            'cloud-service', 'some-region', 'foo.vhd', system_config,
            network_config, 'some-label'
        )
        mock_os_disk.assert_called_once_with(
            'foo.vhd', 'https://bob.blob.core.windows.net/foo/foo.vhd_instance'
        )
        mock_vm_create.assert_called_once_with(
            deployment_slot='production',
            role_size='Small',
            deployment_name='cloud-service',
            service_name='cloud-service',
            os_virtual_hard_disk=os_disk,
            label='some-label',
            system_config=system_config,
            role_name='cloud-service',
            network_config=network_config,
            provision_guest_agent=True,
            media_location='some-region'
        )
        assert result['instance_name'] == 'some-host'

    @patch('azurectl.virtual_machine.ServiceManagementService.delete_deployment')
    def test_delete_instance(self, mock_delete_deployment):
        self.vm.delete_instance('cloud-service', 'foo')
        mock_delete_deployment.assert_called_once_with(
            'cloud-service', 'foo'
        )

    @patch('azurectl.virtual_machine.ServiceManagementService.create_virtual_machine_deployment')
    @raises(AzureVmCreateError)
    def test_create_instance_raise_vm_create_error(self, mock_vm_create):
        mock_vm_create.side_effect = AzureVmCreateError
        result = self.vm.create_instance(
            'foo', 'some-region', 'foo.vhd',
            self.vm.create_linux_configuration()
        )
        assert result['request_id'] < 0

    @patch('azurectl.virtual_machine.ServiceManagementService.delete_deployment')
    @raises(AzureVmDeleteError)
    def test_delete_instance_raise_vm_delete_error(self, modk_delete):
        modk_delete.side_effect = AzureVmDeleteError
        self.vm.delete_instance('cloud-service', 'foo')
