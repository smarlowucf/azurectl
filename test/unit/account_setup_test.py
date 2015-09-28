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
        self.orig_data = {
            'default': {
                'name': 'bob'
            },
            'bob': {
                'storage_account_name': 'bob',
                'storage_container_name': 'foo',
                'publishsettings': '../data/publishsettings'
            },
            'foo': {
                'storage_account_name': 'bob',
                'publishsettings': '../data/publishsettings',
                'storage_container_name': 'foo'
            }
        }
        self.delete_data = {
            'default': {
                'name': 'bob'
            },
            'bob': {
                'storage_account_name': 'bob',
                'storage_container_name': 'foo',
                'publishsettings': '../data/publishsettings'
            }
        }
        self.add_data = {
            'default': {
                'name': 'bob'
            },
            'bob': {
                'storage_account_name': 'bob',
                'storage_container_name': 'foo',
                'publishsettings': '../data/publishsettings'
            },
            'foo': {
                'storage_account_name': 'bob',
                'publishsettings': '../data/publishsettings',
                'storage_container_name': 'foo'
            },
            'xxx': {
                'subscription_id': '1234',
                'storage_account_name': 'storage',
                'publishsettings': '../data/publishsettings',
                'storage_container_name': 'container'
            }
        }

    def test_list(self):
        assert self.setup.list() == self.orig_data

    @mock.patch('__builtin__.open')
    def test_add(self, mock_open):
        self.setup.add(
            'xxx', '../data/publishsettings', 'storage', 'container', '1234'
        )
        assert mock_open.called
        assert self.setup.list() == self.add_data

    @mock.patch('__builtin__.open')
    def test_add_first_account_as_default(self, mock_open):
        setup = AccountSetup('../data/config.new')
        setup.add(
            'xxx', '../data/publishsettings', 'storage', 'container', '1234'
        )
        assert setup.list()['default']['name'] == 'xxx'

    @patch('__builtin__.open')
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_add_creates_dir(self, mock_makedirs, mock_exists, mock_open):
        mock_exists.return_value = False
        self.setup.add(
            'xxx', '../data/publishsettings', 'storage', 'container', '1234'
        )
        assert mock_open.called
        assert self.setup.list() == self.add_data
        assert mock_exists.called
        assert mock_makedirs.called

    @patch('__builtin__.open')
    def test_set_default_account(self, mock_open):
        self.setup.set_default_account('foo')
        assert self.setup.list()['default']['name'] == 'foo'
        assert self.setup.set_default_account('foofoo') == False

    @mock.patch('__builtin__.open')
    def test_remove(self, mock_open):
        self.setup.remove('foo')
        assert mock_open.called
        assert self.setup.list() == self.delete_data

    @mock.patch('__builtin__.open')
    def test_remove_default_account(self, mock_open):
        assert self.setup.remove('bob') == False

    def test_remove_section_does_not_exist(self):
        assert self.setup.remove('foofoo') == False

    @raises(AzureConfigWriteError)
    def test_write_raise(self):
        self.setup.filename = '/proc/xxx'
        self.setup.remove('foo')

    @raises(AzureConfigParseError)
    def test_parse_raise(self):
        AccountSetup('../data/blob.xz')

    @raises(AzureConfigPublishSettingsError)
    def test_add_raise_publish_settings_error(self):
        self.setup.add(
            'xxx', '../data/does-not-exist', 'storage', 'container'
        )

    @raises(AzureConfigAddAccountSectionError)
    def test_add_raise(self):
        self.setup.add(
            'default', '../data/publishsettings', 'storage', 'container'
        )
