import sys
import mock
from collections import namedtuple
from mock import patch
from mock import call


from test_helper import *

from azurectl.azure_account import AzureAccount
from azurectl.config import Config
from azurectl.azurectl_exceptions import *
from azurectl.storage_account import StorageAccount

import azurectl


class TestStorageAccount:
    def setup(self):
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
            return_value='.blob.test.url'
        )
        account.storage_key = mock.Mock()

        self.containers_list = ['container_a', 'container_b']
        self.mock_storage_service = mock.Mock(
            storage_service_keys=None,
            storage_service_properties=mock.Mock(
                status='Created',
                account_type='Standard_GRS',
                description='mock storage service',
                geo_secondary_region='West US',
                creation_time='2015-12-09T07:53:54Z',
                geo_primary_region='East US 2',
                label='mockstorageservice',
                status_of_primary='Available',
                location='East US 2',
                affinity_group='',
                last_geo_failover_time='',
                status_of_secondary='Available',
                endpoints=[
                    'https://mockstorageservice.blob.core.windows.net/',
                    'https://mockstorageservice.queue.core.windows.net/',
                    'https://mockstorageservice.table.core.windows.net/',
                    'https://mockstorageservice.file.core.windows.net/'
                ],
                geo_replication_enabled='True'
            ),
            url=(
                'https://management.core.windows.net/' +
                '00000000-0000-0000-0000-000000000000/services/' +
                'storageservices/mockstorageservice'
            ),
            service_name='mockstorageservice',
            capabilities='None',
            extended_properties={
                'ResourceGroup': 'Default-Storage-EastUS2',
                'ResourceLocation': 'East US 2'
            },
            containers=None
        )
        self.keyed_service = mock.Mock(
            storage_service_keys=mock.Mock(
                primary='1234567890abcdef==',
                secondary='fedcba0987654321=='
            )
        )
        self.expected_list_result = [{
            "backup": {
                "backup-region": "West US",
                "backup-region-status": "Available",
                "last-failover": "",
                "status": "Available"
            },
            "backup-strategy": "--geo-redundant",
            "description": "mock storage service",
            "endpoints": [
                "https://mockstorageservice.blob.core.windows.net/",
                "https://mockstorageservice.queue.core.windows.net/",
                "https://mockstorageservice.table.core.windows.net/",
                "https://mockstorageservice.file.core.windows.net/"
            ],
            "label": "mockstorageservice",
            "name": "mockstorageservice",
            "region": "East US 2",
            "status": "Created"
        }]
        self.expected_show_result = {
            "backup": {
                "backup-region": "West US",
                "backup-region-status": "Available",
                "last-failover": "",
                "status": "Available"
            },
            "backup-strategy": "--geo-redundant",
            "containers": self.containers_list,
            "description": "mock storage service",
            "endpoints": [
                "https://mockstorageservice.blob.core.windows.net/",
                "https://mockstorageservice.queue.core.windows.net/",
                "https://mockstorageservice.table.core.windows.net/",
                "https://mockstorageservice.file.core.windows.net/"
            ],
            "keys": {
                "primary": self.keyed_service.storage_service_keys.primary,
                "secondary": self.keyed_service.storage_service_keys.secondary
            },
            "label": "mockstorageservice",
            "name": "mockstorageservice",
            "region": "East US 2",
            "status": "Created"
        }

        self.my_request = mock.Mock(request_id=42)

        self.storage_account = StorageAccount(account)

    @patch('azurectl.storage_account.ServiceManagementService.list_storage_accounts')
    def test_list(self, mock_list_accounts):
        mock_list_accounts.return_value = [self.mock_storage_service]
        result = self.storage_account.list()
        assert result == self.expected_list_result

    @patch('azurectl.storage_account.ServiceManagementService.list_storage_accounts')
    @raises(AzureStorageAccountListError)
    def test_list_error(self, mock_list_accounts):
        mock_list_accounts.side_effect = Exception
        self.storage_account.list()

    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_keys')
    @patch('azurectl.storage_account.Container.list')
    def test_show(self, mock_container_list, mock_storage_keys, mock_show_account):
        mock_show_account.return_value = self.mock_storage_service
        mock_storage_keys.return_value = self.keyed_service
        mock_container_list.return_value = self.containers_list
        result = self.storage_account.show(
            self.mock_storage_service.service_name
        )
        assert result == self.expected_show_result

    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @raises(AzureStorageAccountShowError)
    def test_show_error(self, mock_show_account):
        mock_show_account.side_effect = Exception
        self.storage_account.show('mockstorageservice')

    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_keys')
    @raises(AzureStorageAccountShowError)
    def test_show_add_keys_error(self, mock_storage_keys, mock_show_account):
        mock_show_account.return_value = self.mock_storage_service
        mock_storage_keys.side_effect = Exception
        self.storage_account.show('mockstorageservice')

    @patch('azurectl.storage_account.ServiceManagementService.create_storage_account')
    def test_create(self, mock_create_account):
        mock_create_account.return_value = self.my_request
        result = self.storage_account.create(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant'
        )
        assert result == self.my_request.request_id

    @patch('azurectl.storage_account.ServiceManagementService.create_storage_account')
    @raises(AzureStorageAccountCreateError)
    def test_create_error(self, mock_create_account):
        mock_create_account.side_effect = Exception
        result = self.storage_account.create(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant'
        )

    @patch('azurectl.storage_account.ServiceManagementService.update_storage_account')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_keys')
    @patch('azurectl.storage_account.Container.list')
    def test_basic_update(
        self,
        mock_container_list,
        mock_storage_keys,
        mock_show_account,
        mock_update_account
    ):
        mock_update_account.return_value = self.my_request
        mock_show_account.return_value = self.mock_storage_service
        mock_storage_keys.return_value = self.keyed_service
        mock_container_list.return_value = self.containers_list
        result = self.storage_account.update(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant'
        )
        assert result == self.expected_show_result

    @patch('azurectl.storage_account.ServiceManagementService.update_storage_account')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @raises(AzureStorageAccountUpdateError)
    def test_update_error(self, mock_account_properties, mock_update_account):
        mock_update_account.side_effect = Exception
        result = self.storage_account.update(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant'
        )

    @patch('azurectl.storage_account.ServiceManagementService.regenerate_storage_account_keys')
    @patch('azurectl.storage_account.ServiceManagementService.update_storage_account')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_properties')
    @patch('azurectl.storage_account.ServiceManagementService.get_storage_account_keys')
    @patch('azurectl.storage_account.Container.list')
    def test_update_keys(
        self,
        mock_container_list,
        mock_storage_keys,
        mock_show_account,
        mock_update_account,
        mock_regenerate_keys
    ):
        mock_update_account.return_value = self.my_request
        mock_regenerate_keys.return_value = self.my_request
        mock_show_account.return_value = self.mock_storage_service
        mock_storage_keys.return_value = self.keyed_service
        mock_container_list.return_value = self.containers_list

        # primary key
        result = self.storage_account.update(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant',
            regenerate_primary_key=True
        )
        mock_regenerate_keys.assert_called_with(
            'mockstorageservice',
            'Primary'
        )

        # secondary key
        result = self.storage_account.update(
            'mockstorageservice',
            None,
            None,
            '--locally-redundant',
            regenerate_secondary_key=True
        )
        mock_regenerate_keys.assert_called_with(
            'mockstorageservice',
            'Secondary'
        )

    @patch('azurectl.storage_account.ServiceManagementService.delete_storage_account')
    def test_delete(self, mock_delete_account):
        mock_delete_account.return_value = self.my_request

        result = self.storage_account.delete('mockstorageservice')
        assert result == self.my_request.request_id

    @patch('azurectl.storage_account.ServiceManagementService.delete_storage_account')
    @raises(AzureStorageAccountDeleteError)
    def test_delete_error(self, mock_delete_account):
        mock_delete_account.side_effect = Exception

        self.storage_account.delete('mockstorageservice')
