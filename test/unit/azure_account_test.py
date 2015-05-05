import mock
from mock import patch
from nose.tools import *

import nose_helper

from azure_cli.azurectl_exceptions import *

import azure_cli

from azure_cli.azure_account import AzureAccount

from collections import namedtuple


class TestAzureAccount:
    def setup(self):
        self.account = AzureAccount('default', '../data/config')
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        self.publishsettings = credentials(
            private_key='abc',
            certificate='abc',
            subscription_id='4711'
        )
        azure_cli.azure_account.load_pkcs12 = mock.Mock()

    def test_storage_name(self):
        assert self.account.storage_name() == 'bob'

    def test_storage_container(self):
        assert self.account.storage_container() == 'foo'

    @raises(AzureSubscriptionParseError)
    def test_publishsettings_missing_subscription(self):
        account_invalid = AzureAccount(
            'default', '../data/config.invalid_publishsettings_subscription'
        )
        account_invalid.publishsettings()

    @raises(AzureSubscriptionDecodeError)
    def test_publishsettings_invalid_cert(self):
        account_invalid = AzureAccount(
            'default', '../data/config.invalid_publishsettings_cert'
        )
        account_invalid.publishsettings()

    @patch('azure_cli.azure_account.dump_privatekey')
    @patch('azure_cli.azure_account.dump_certificate')
    def test_publishsettings(self, mock_dump_pkey, mock_dump_certificate):
        mock_dump_pkey.return_value = 'abc'
        mock_dump_certificate.return_value = 'abc'
        assert self.account.publishsettings() == self.publishsettings

    @patch(
        'azure_cli.azure_account.ServiceManagementService' +
        '.get_storage_account_keys'
    )
    def test_storage_key(self, mock_service):
        self.account.publishsettings = mock.Mock(
            return_value=self.publishsettings
        )
        primary = namedtuple(
            'primary', 'primary'
        )
        keys = namedtuple(
            'storage_service_keys', 'storage_service_keys'
        )
        service_result = keys(storage_service_keys=primary(primary='foo'))
        mock_service.return_value = service_result
        assert self.account.storage_key() == 'foo'

    @patch(
        'azure_cli.azure_account.ServiceManagementService' +
        '.list_storage_accounts'
    )
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
