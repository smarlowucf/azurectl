import mock
from nose.tools import *

import nose_helper

from azure_cli.azurectl_exceptions import *
from azure_cli.config import Config


class TestConfig:
    def setup(self):
        self.config = Config('default', '../data/config')

    def test_get_option(self):
        assert self.config.get_option('storage_account_name') == 'bob'

    @raises(AzureConfigParseError)
    def test_parse_error(self):
        config = Config('default', '../data/config_parse_error')
