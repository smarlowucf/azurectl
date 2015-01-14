import mock
from nose.tools import *
from azure_cli.exceptions import *

import azure_cli

from azure_cli.service_account import ServiceAccount

from collections import namedtuple

class Fake_pkcs12:
    def get_privatekey(self):
        return 'abc'

    def get_certificate(self):
        return 'abc'

class TestServiceAccount:
    def setup(self):
        self.account = ServiceAccount('default', '../data/config')
        azure_cli.service_account.load_pkcs12 = mock.Mock(
            return_value=Fake_pkcs12()
        )
        azure_cli.service_account.dump_privatekey = mock.Mock(
            return_value='abc'
        )
        azure_cli.service_account.dump_certificate = mock.Mock(
            return_value='abc'
        )

    def test_get_private_key(self):
        assert self.account.get_private_key() == 'abc'

    def test_get_cert(self):
        assert self.account.get_cert() == 'abc'

    def test_get_subscription_id(self):
        assert self.account.get_subscription_id() == '4711'
