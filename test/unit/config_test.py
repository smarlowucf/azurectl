import mock
from nose.tools import *
from mock import patch

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.config import Config

import os


class TestConfig:
    def setup(self):
        self.config = Config('bob', 'East US 2', None, None, '../data/config')

    def test_get_account_name(self):
        assert self.config.get_account_name() == 'bob'

    def test_get_region_name(self):
        assert self.config.get_region_name() == 'East US 2'

    def test_get_storage_account_name(self):
        assert self.config.get_storage_account_name() == 'bob'

    def test_get_storage_container_name(self):
        assert self.config.get_storage_container_name() == 'foo'

    @raises(AzureConfigVariableNotFound)
    def test_get_subscription_id_missing(self):
        assert self.config.get_subscription_id()

    @raises(AzureConfigVariableNotFound)
    def test_get_publishsettings_file_name_missing(self):
        config = Config(
            'bob', 'East US 2', None, None,
            '../data/config.missing_region_data'
        )
        config.get_storage_account_name()

    def test_get_publishsettings_file_name(self):
        assert self.config.get_publishsettings_file_name() == \
            '../data/publishsettings'

    @raises(AzureConfigSectionNotFound)
    def test_account_not_found(self):
        Config('xxx', 'East US 2', None, None, '../data/config')

    @raises(AzureConfigRegionNotFound)
    def test_region_not_referenced(self):
        self.config.region_name = None
        self.config.get_storage_account_name()

    @raises(AzureConfigAccountNotFound)
    def test_account_not_referenced(self):
        self.config.account_name = None
        self.config.get_publishsettings_file_name()

    @raises(AzureConfigParseError)
    def test_parse_error(self):
        Config('bob', 'East US 2', None, None, '../data/config_parse_error')

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_account_file_not_found_in_config(self, mock_isfile):
        mock_isfile.return_value = False
        Config('bob', 'East US 2', None, None, '../data/config')

    @raises(AzureAccountLoadFailed)
    @patch('os.path.isfile')
    def test_no_default_config_file_found(self, mock_isfile):
        mock_isfile.return_value = False
        Config()

    @raises(AzureAccountDefaultSectionNotFound)
    def test_no_default_section_in_config(self):
        Config(None, 'East US 2', None, None, '../data/config.no_default')

    @raises(AzureStorageAccountInvalid)
    def test_invalid_storage_account_name(self):
        self.config.storage_account_name = 'xxx'
        self.config.get_storage_account_name()

    @raises(AzureStorageAccountInvalid)
    def test_invalid_storage_container_name(self):
        self.config.storage_container_name = 'xxx'
        self.config.get_storage_container_name()
