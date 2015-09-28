import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import *

import azurectl

from azurectl.azure_account import AzureAccount
from azurectl.config import Config

from collections import namedtuple


class TestAzureAccount:
    def setup(self):
        self.account = AzureAccount(
            Config('bob', '../data/config')
        )
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        self.publishsettings = credentials(
            private_key='abc',
            certificate='abc',
            subscription_id='4711'
        )
        azurectl.azure_account.load_pkcs12 = mock.Mock()

    @raises(AzureServiceManagementError)
    @patch('azurectl.azure_account.ServiceManagementService')
    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    def test_service_error(
        self, mock_dump_pkey, mock_dump_certificate, mock_service
    ):
        mock_dump_pkey.return_value = 'abc'
        mock_dump_certificate.return_value = 'abc'
        mock_service.side_effect = AzureServiceManagementError
        self.account.storage_names()

    def test_storage_name(self):
        assert self.account.storage_name() == 'bob'

    def test_storage_container(self):
        assert self.account.storage_container() == 'foo'

    @raises(AzureSubscriptionParseError)
    def test_empty_publishsettings(self):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.empty_publishsettings')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionParseError)
    def test_missing_publishsettings(self):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.missing_publishsettings')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionIdNotFound)
    def test_publishsettings_missing_subscription(self):
        account_invalid = AzureAccount(
            Config(
                'bob', '../data/config.invalid_publishsettings_subscription'
            )
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionPrivateKeyDecodeError)
    def test_publishsettings_invalid_cert(self):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.invalid_publishsettings_cert')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionCertificateDecodeError)
    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    def test_subscription_cert_decode_error(
        self, mock_dump_certificate, mock_dump_pkey
    ):
        mock_dump_pkey.return_value = 'abc'
        mock_dump_certificate.side_effect = AzureSubscriptionCertificateDecodeError
        self.account.publishsettings()

    @raises(AzureManagementCertificateNotFound)
    def test_subscription_management_cert_not_found(self):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.missing_publishsettings_cert')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionIdNotFound)
    @patch('azurectl.azure_account.load_pkcs12')
    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    @patch('base64.b64decode')
    def test_subscription_id_missing(
        self, base64_decode, mock_dump_certificate,
        mock_dump_pkey, mock_pkcs12
    ):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.missing_publishsettings_id')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionIdNotFound)
    @patch('azurectl.azure_account.load_pkcs12')
    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    @patch('base64.b64decode')
    def test_config_subscription_id_not_found_in_publishsettings(
        self, base64_decode, mock_dump_certificate,
        mock_dump_pkey, mock_pkcs12
    ):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.missing_set_subscription_id')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionIdNotFound)
    @patch('azurectl.azure_account.load_pkcs12')
    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    @patch('base64.b64decode')
    def test_config_subscription_id_missing(
        self, base64_decode, mock_dump_certificate,
        mock_dump_pkey, mock_pkcs12
    ):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.set_subscription_id_missing_id')
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionPKCS12DecodeError)
    def test_subscription_pkcs12_error(self):
        account_invalid = AzureAccount(
            Config('bob', '../data/config.corrupted_p12_cert')
        )
        account_invalid.publishsettings()

    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    def test_publishsettings(self, mock_dump_certificate, mock_dump_pkey):
        mock_dump_pkey.return_value = 'abc'
        mock_dump_certificate.return_value = 'abc'
        assert self.account.publishsettings() == self.publishsettings

    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    def test_publishsettings_with_multiple_subscriptions_defaults_to_first(
        self,
        mock_dump_certificate,
        mock_dump_pkey
    ):
        account = AzureAccount(
            Config('bob', '../data/config.multiple_subscriptions_no_id')
        )
        assert account.publishsettings().subscription_id == 'first'

    @patch('azurectl.azure_account.dump_privatekey')
    @patch('azurectl.azure_account.dump_certificate')
    def test_config_specifies_subscription_in_publishsettings(
        self,
        mock_dump_certificate,
        mock_dump_pkey
    ):
        account = AzureAccount(
            Config('bob', '../data/config.multiple_subscriptions_set_id')
        )
        assert account.publishsettings().subscription_id == 'second'

    @patch('azurectl.azure_account.ServiceManagementService.get_storage_account_keys')
    def test_storage_key(self, mock_get_keys):
        self.account.publishsettings = mock.Mock(
            return_value=self.publishsettings
        )
        primary = namedtuple(
            'primary', 'primary'
        )
        keys = namedtuple(
            'storage_service_keys', 'storage_service_keys'
        )
        get_keys_result = keys(storage_service_keys=primary(primary='foo'))
        mock_get_keys.return_value = get_keys_result
        assert self.account.storage_key() == 'foo'

    @raises(AzureServiceManagementError)
    @patch('azurectl.azure_account.ServiceManagementService.get_storage_account_keys')
    def test_storage_key_error(self, mock_get_keys):
        self.account.publishsettings = mock.Mock(
            return_value=self.publishsettings
        )
        mock_get_keys.side_effect = AzureServiceManagementError
        self.account.storage_key()

    @patch('azurectl.azure_account.ServiceManagementService.list_storage_accounts')
    def test_storage_names(self, mock_service):
        self.account.publishsettings = mock.Mock(
            return_value=self.publishsettings
        )
        service_result = []
        names = namedtuple(
            'service_name', 'service_name'
        )
        service_result.append(names(service_name='foo'))
        mock_service.return_value = service_result
        assert self.account.storage_names() == ['foo']
        service = self.account.service
        # calling again and see if the same ServiceManagementService is used
        self.account.storage_names()
        assert self.account.get_service() == self.account.service

    @patch('azurectl.azure_account.ServiceManagementService.list_role_sizes')
    def test_instance_types(self, mock_service):
        self.account.publishsettings = mock.Mock(
            return_value=self.publishsettings
        )
        service_result = []
        names = namedtuple(
            'names',
            'name memory_in_mb cores max_data_disk_count \
             virtual_machine_resource_disk_size_in_mb'
        )
        service_result.append(names(
            name='foo',
            memory_in_mb=1,
            cores=2,
            max_data_disk_count=3,
            virtual_machine_resource_disk_size_in_mb=4
        ))
        mock_service.return_value = service_result
        x = self.account.instance_types()
        assert self.account.instance_types() == [
            {'foo': {
                'cores': 2,
                'max_disk_count': 3,
                'disk_size': '4MB',
                'memory': '1MB'
            }}
        ]
