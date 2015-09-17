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

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_no_default_config_file_found(self, mock_isfile):
        mock_isfile.return_value = False
        Config()

    @patch('os.path.isfile')
    @patch('ConfigParser.ConfigParser.has_section')
    def test_home_path_linux(self, mock_section, mock_isfile):
        mock_isfile.return_value = True
        mock_section.return_value = True
        config = Config()
        assert config.config_file == \
            os.environ['HOME'] + '/.config/azurectl/config'

    @patch('os.path.isfile')
    @patch('ConfigParser.ConfigParser.has_section')
    def test_home_path_win(self, mock_section, mock_isfile):
        mock_isfile.return_value = True
        mock_section.return_value = True
        with patch.dict('os.environ', {'HOMEPATH': 'foo'}):
            config = Config(None, None, 'win')
            assert config.config_file == \
                os.environ['HOMEPATH'] + '/.config/azurectl/config'
        with patch.dict('os.environ', {'UserProfile': 'foo'}):
            config = Config(None, None, 'win')
            assert config.config_file == \
                os.environ['UserProfile'] + '/.config/azurectl/config'
