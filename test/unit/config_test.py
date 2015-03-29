import mock
from nose.tools import *

from azure_cli.config import Config


class TestConfig:
    def setup(self):
        self.config = Config('default', '../data/config')

    def test_read(self):
        assert self.config.get_option('storage_account_name') == 'bob'
