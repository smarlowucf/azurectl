import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import (
    AzureConfigParseError,
    AzureConfigAddAccountSectionError,
    AzureConfigAddRegionSectionError,
    AzureConfigPublishSettingsError,
    AzureConfigWriteError
)
from azurectl.account_setup import AccountSetup

import azurectl


class TestAccountSetup:
    def setup(self):
        self.setup = AccountSetup('../data/config')
        self.orig_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                },
                'foo': {
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'bob'
                },
                'West US 1': {
                    'default_storage_container': 'bar',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'joe'
                }
            }
        }
        self.delete_account_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_account': 'bob',
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar'
                },
                'West US 1': {
                    'default_storage_container': 'bar',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'joe'
                }
            }
        }
        self.delete_region_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                },
                'foo': {
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_account': 'bob',
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar'
                }
            }
        }
        self.add_account_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                },
                'foo': {
                    'publishsettings': '../data/publishsettings'
                },
                'xxx': {
                    'subscription_id': '1234',
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_account': 'bob',
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar'
                },
                'West US 1': {
                    'default_storage_container': 'bar',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'joe'
                }
            }
        }
        self.add_region_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                },
                'foo': {
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_account': 'bob',
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar'
                },
                'West US 1': {
                    'default_storage_container': 'bar',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'joe'
                },
                'some-region': {
                    'default_storage_account': 'storage',
                    'default_storage_container': 'container',
                    'storage_accounts': 'storage,joe',
                    'storage_containers': 'container,bar'
                }
            }
        }
        self.configure_data = {
            'DEFAULT': {
                'account': 'bob',
                'region': 'East US 2'
            },
            'account': {
                'bob': {
                    'publishsettings': '../data/publishsettings'
                },
                'foo': {
                    'publishsettings': '../data/publishsettings'
                },
                'xxx': {
                    'subscription_id': '1234',
                    'publishsettings': '../data/publishsettings'
                }
            },
            'region': {
                'East US 2': {
                    'default_storage_account': 'bob',
                    'default_storage_container': 'foo',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar'
                },
                'West US 1': {
                    'default_storage_container': 'bar',
                    'storage_accounts': 'bob,joe',
                    'storage_containers': 'foo,bar',
                    'default_storage_account': 'joe'
                },
                'some-region': {
                    'default_storage_account': 'storage',
                    'default_storage_container': 'container',
                    'storage_accounts': 'storage,joe',
                    'storage_containers': 'container,bar'
                }
            }
        }

    def test_list(self):
        assert self.setup.list() == self.orig_data

    def test_configure_account_and_region(self):
        self.setup.configure_account_and_region(
            'xxx', '../data/publishsettings',
            'some-region', 'storage', 'container',
            ['storage', 'joe'], ['container', 'bar'],
            '1234'
        )
        assert self.setup.list() == self.configure_data

    def test_add_account(self):
        self.setup.add_account(
            'xxx', '../data/publishsettings', '1234'
        )
        assert self.setup.list() == self.add_account_data

    def test_add_region(self):
        self.setup.add_region(
            'some-region', 'storage', 'container',
            ['storage', 'joe'], ['container', 'bar']
        )
        assert self.setup.list() == self.add_region_data

    def test_add_first_account_as_default(self):
        setup = AccountSetup('../data/config.new')
        setup.add_account(
            'some-account', '../data/publishsettings', '1234'
        )
        assert setup.list()['DEFAULT']['account'] == 'some-account'

    def test_add_first_region_as_default(self):
        setup = AccountSetup('../data/config.new')
        setup.add_region(
            'some-region', 'storage', 'container'
        )
        assert setup.list()['DEFAULT']['region'] == 'some-region'
        assert setup.list()['region']['some-region']['storage_accounts'] == \
            'storage'
        assert setup.list()['region']['some-region']['storage_containers'] == \
            'container'

    @patch('__builtin__.open')
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_add_creates_dir(self, mock_makedirs, mock_exists, mock_open):
        mock_exists.return_value = False
        self.setup.write()
        assert mock_open.called
        assert mock_exists.called
        assert mock_makedirs.called

    def test_set_default_account(self):
        self.setup.set_default_account('foo')
        assert self.setup.list()['DEFAULT']['account'] == 'foo'
        assert self.setup.set_default_account('foofoo') == False

    def test_set_default_region(self):
        self.setup.set_default_region('West US 1')
        assert self.setup.list()['DEFAULT']['region'] == 'West US 1'
        assert self.setup.set_default_region('foofoo') == False

    def test_remove_account(self):
        self.setup.remove_account('foo')
        assert self.setup.list() == self.delete_account_data

    def test_remove_region(self):
        self.setup.remove_region('West US 1')
        assert self.setup.list() == self.delete_region_data

    def test_remove_default_account(self):
        assert self.setup.remove_account('bob') == False

    def test_remove_default_region(self):
        assert self.setup.remove_region('East US 2') == False

    def test_remove_section_does_not_exist(self):
        assert self.setup.remove_account('foofoo') == False
        assert self.setup.remove_region('foofoo') == False

    @raises(AzureConfigWriteError)
    @patch('__builtin__.open')
    def test_write_raise(self, mock_open):
        mock_open.side_effect = AzureConfigWriteError
        self.setup.filename = '/some-config'
        self.setup.write()

    @raises(AzureConfigParseError)
    def test_parse_raise(self):
        AccountSetup('../data/blob.xz')

    @raises(AzureConfigPublishSettingsError)
    def test_add_raise_publish_settings_error(self):
        self.setup.add_account(
            'xxx', '../data/does-not-exist'
        )

    @raises(AzureConfigAddAccountSectionError)
    def test_add_account_raise(self):
        self.setup.add_account(
            'default', '../data/publishsettings'
        )

    @raises(AzureConfigAddRegionSectionError)
    def test_add_region_raise(self):
        self.setup.add_region(
            'default', 'some-region', 'storage'
        )
