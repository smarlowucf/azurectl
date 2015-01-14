from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.service_account import ServiceAccount

class TestServiceAccount:
    def setup(self):
        self.service = ServiceAccount('default', '../data/config')

    def test_get_account_subscription_id(self):
        assert self.service.get_account_subscription_id() == 'id'

    def test_get_account_subscription_cert(self):
        assert self.service.get_account_subscription_cert() == '/some/cert.pem'
