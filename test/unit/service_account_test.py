import mock
from nose.tools import *
from azure_cli.exceptions import *
from azure_cli.service_account import ServiceAccount

class TestServiceAccount:
    def setup(self):
        self.account = ServiceAccount('default', '../data/config')

    def test_get_private_key(self):
        pass

    def test_get_cert(self):
        pass

    def get_subscription_id(self):
        pass
