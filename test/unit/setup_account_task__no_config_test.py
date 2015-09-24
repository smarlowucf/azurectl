import mock
import os
import sys
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azurectl_exceptions import *
from azurectl.setup_account_task import SetupAccountTask


class TestSetupAccountTask_NoConfig:

    @patch('os.path.isfile')
    @patch('azurectl.setup_account_task.ConfigFilePath.default_new_config')
    @patch('azurectl.setup_account_task.AccountSetup.add')
    def test_create_new_account(
        self,
        mock_add,
        mock_default_new_config,
        mock_isfile
    ):
        sys.argv = [
            sys.argv[0],
            'setup', 'account', 'add',
            '--name', 'default',
            '--publish-settings-file', 'file',
            '--storage-account-name', 'foo',
            '--container-name', 'foo'
        ]

        mock_isfile.return_value = False
        mock_default_new_config.return_value = '/foo/config'

        task = SetupAccountTask()
        task.process()
        task.setup.add.assert_called_once_with(
            task.command_args['--name'],
            task.command_args['--publish-settings-file'],
            task.command_args['--storage-account-name'],
            task.command_args['--container-name'],
            None
        )
        assert task.config_file == "/foo/config"

    @patch('os.path.isfile')
    @raises(AzureAccountLoadFailed)
    def test_no_default_config_file_unless_adding(self, mock_isfile):
        sys.argv = [
            sys.argv[0],
            'setup', 'account', 'list'
        ]

        mock_isfile.return_value = False
        task = SetupAccountTask()
        task.process()
