import sys
import mock
from collections import namedtuple
from mock import patch
from mock import call
from nose.tools import *

import nose_helper

from azurectl.azure_account import AzureAccount
from azurectl.config import Config
from azurectl.azurectl_exceptions import *
from azurectl.reserved_ip import ReservedIp

import azurectl


class TestReservedIp:
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

        MyStruct = namedtuple(
            'MyStruct',
            'name address label state in_use service_name deployment_name \
            location'
        )

        self.list_ips = [MyStruct(
            name='some-name',
            address='1.2.3.4',
            label='',
            state='Created',
            in_use=True,
            service_name='foo',
            deployment_name='bar',
            location='Region'
        )]

        self.result_list = [{
            'name': 'some-name',
            'address': '1.2.3.4',
            'state': 'Created',
            'in_use': True,
            'cloud_service_name': 'foo',
            'instance_name': 'bar',
            'region': 'Region'
        }]

        self.reserved_ip = ReservedIp(account)

    @patch('azurectl.reserved_ip.ServiceManagementService.list_reserved_ip_addresses')
    def test_list(self, mock_list_ips):
        mock_list_ips.return_value = self.list_ips
        assert self.reserved_ip.list() == self.result_list

    @patch('azurectl.reserved_ip.ServiceManagementService.list_reserved_ip_addresses')
    @raises(AzureReservedIpListError)
    def test_list_raises_error(self, mock_list_ips):
        mock_list_ips.side_effect = Exception
        self.reserved_ip.list()
