import mock
from nose.tools import *
from mock import patch

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.config import Config

import os


class TestConfig:
    def setup(self):
        self.config = Config('default', '../data/config')

    def test_get_option(self):
        assert self.config.get_option('storage_account_name') == 'bob'

    @raises(AzureConfigParseError)
    def test_parse_error(self):
        Config('default', '../data/config_parse_error')

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_account_file_not_found_in_config(self, mock_isfile):
        mock_isfile.return_value = False
        Config('default', '../data/config')

    @raises(AzureAccountNotFound)
    def test_account_name_not_found_in_config(self):
        Config('foo', '../data/config')

    @raises(AzureAccountValueNotFound)
    def test_get_option_not_found(self):
        self.config.get_option('foo')

    def test_home_path_linux(self):
        config = Config('default', '../data/config')
        assert config.DEFAULT_CONFIG == os.environ['HOME'] + '/.azurectl/config'

    def test_home_path_win(self):
        # sorry, no idea how to mock sys.platform
        pass
