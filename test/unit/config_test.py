import mock
from nose.tools import *
from mock import patch

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.config import Config

import os


class TestConfig:
    def setup(self):
        self.config = Config('bob', '../data/config')

    def test_get_option(self):
        assert self.config.get_option('storage_account_name') == 'bob'

    @raises(AzureConfigParseError)
    def test_parse_error(self):
        Config('bob', '../data/config_parse_error')

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_account_file_not_found_in_config(self, mock_isfile):
        mock_isfile.return_value = False
        Config('bob', '../data/config')

    @raises(AzureAccountNotFound)
    def test_account_name_not_found_in_config(self):
        Config('foofoo', '../data/config')

    @raises(AzureAccountValueNotFound)
    def test_get_option_not_found(self):
        self.config.get_option('foo')

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_no_default_config_file_found(self, mock_isfile):
        mock_isfile.return_value = False
        Config()

    @raises(AzureAccountDefaultSectionNotFound)
    def test_no_default_section_in_config(self):
        Config(None, '../data/config.no_default')
