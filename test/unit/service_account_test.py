import mock
from mock import patch
from nose.tools import *
from azure_cli.exceptions import *

import azure_cli

from azure_cli.service_account import ServiceAccount

class TestServiceAccount:
    def setup(self):
        self.account = ServiceAccount('default', '../data/config')
        azure_cli.service_account.load_pkcs12 = mock.Mock()

    @patch('azure_cli.service_account.dump_privatekey')
    def test_get_private_key(self, mock_dump_privatekey):
        mock_dump_privatekey.return_value = 'abc'
        assert self.account.get_private_key() == 'abc'

    @patch('azure_cli.service_account.dump_certificate')
    def test_get_cert(self, mock_dump_certificate):
        mock_dump_certificate.return_value = 'abc'
        assert self.account.get_cert() == 'abc'

    def test_get_subscription_id(self):
        assert self.account.get_subscription_id() == '4711'
