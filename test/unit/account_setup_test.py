import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.account_setup import AccountSetup

import azurectl


class TestAccountSetup:
    def setup(self):
        self.setup = AccountSetup('../data/config')
        self.orig_data = {'default': {
            'storage_account_name': 'bob',
            'storage_container_name': 'foo',
            'publishsettings': '../data/publishsettings'}
        }
        self.add_data = {
            'default': {
                'storage_account_name': 'bob',
                'storage_container_name': 'foo',
                'publishsettings': '../data/publishsettings'
            },
            'foo': {
                'storage_account_name': 'storage',
                'publishsettings': '../data/publishsettings',
                'storage_container_name': 'container',
                'subscription_id': '1234'
            }
        }

    def test_list(self):
        assert self.setup.list() == self.orig_data

    @mock.patch('__builtin__.open')
    def test_add(self, mock_open):
        self.setup.add(
            'foo', '../data/publishsettings', 'storage', 'container', '1234'
        )
        assert mock_open.called
        assert self.setup.list() == self.add_data

    @patch('__builtin__.open')
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_add_creates_dir(self, mock_makedirs, mock_exists, mock_open):
        mock_exists.return_value = False

        self.setup.add(
            'foo', '../data/publishsettings', 'storage', 'container', '1234'
        )

        assert mock_open.called
        assert self.setup.list() == self.add_data
        assert mock_exists.called
        assert mock_makedirs.called

    @mock.patch('__builtin__.open')
    def test_remove(self, mock_open):
        self.setup.remove('default')
        assert mock_open.called
        assert self.setup.list() == {}

    def test_remove_section_does_not_exist(self):
        assert self.setup.remove('foofoo') == False

    @raises(AzureConfigWriteError)
    def test_write_raise(self):
        self.setup.filename = '/proc/xxx'
        self.setup.remove('default')

    @raises(AzureConfigParseError)
    def test_parse_raise(self):
        AccountSetup('../data/blob.xz')

    @raises(AzureConfigPublishSettingsError)
    def test_add_raise_publish_settings_error(self):
        self.setup.add(
            'foo', '../data/does-not-exist', 'storage', 'container'
        )

    @raises(AzureConfigAddAccountSectionError)
    def test_add_raise(self):
        self.setup.add(
            'default', '../data/publishsettings', 'storage', 'container'
        )
