import sys
import mock

from mock import patch

import logging

from test_helper import *

import azurectl

from azurectl.cli_task import CliTask
from azurectl.azurectl_exceptions import *


class TestCliTask:
    @raises(SystemExit)
    @patch('azurectl.cli_task.Help.show')
    def test_show_help(self, help_show):
        sys.argv = [
            sys.argv[0], 'help'
        ]
        CliTask()
        help_show.assert_called_once_with('azurectl')

    @patch('azurectl.cli_task.Cli.show_help')
    @patch('azurectl.logger.log.setLevel')
    def test_cli_init(self, mock_loglevel, mock_show_help):
        sys.argv = [
            sys.argv[0],
            '--debug',
            '--region', 'region',
            '--config', 'config',
            'compute', 'storage', 'container', 'list'
        ]
        mock_show_help.return_value = False
        task = CliTask()
        mock_loglevel.assert_called_once_with(logging.DEBUG)

    @patch('azurectl.cli_task.Validations.validate_min_length')
    def test_validate_min_length(self, mock_validation):
        sys.argv = [
            sys.argv[0],
            '--config', 'config',
            'setup', 'account', 'default', '--name', 'test-name0'
        ]
        task = CliTask()
        task.validate_min_length('--name', 5)
        mock_validation.assert_called_once_with('--name', 'test-name0', 5)

    @patch('azurectl.cli_task.Validations.validate_max_length')
    def test_validate_max_length(self, mock_validation):
        sys.argv = [
            sys.argv[0],
            '--config', 'config',
            'setup', 'account', 'default', '--name', 'test-name0'
        ]
        task = CliTask()
        task.validate_max_length('--name', 10)
        mock_validation.assert_called_once_with('--name', 'test-name0', 10)

    @patch('azurectl.cli_task.Cli.show_help')
    @patch('azurectl.cli_task.Config')
    @patch('azurectl.logger.log.setLevel')
    def test_load_config(
        self, mock_loglevel, mock_config, mock_show_help
    ):
        sys.argv = [
            sys.argv[0],
            '--debug',
            '--region', 'region',
            '--config', 'config',
            'compute', 'storage', 'container', 'list'
        ]
        mock_show_help.return_value = False
        task = CliTask()
        task.load_config()
        mock_config.assert_called_once_with(
            None, 'region', None, None, 'config'
        )
        mock_loglevel.assert_called_once_with(logging.DEBUG)

    @patch('azurectl.cli_task.Cli.show_help')
    @patch('azurectl.cli_task.Config')
    @patch('azurectl.logger.log.setLevel')
    @patch('azurectl.cli_task.ConfigFilePath')
    def test_load_config_create_new_account(
        self, mock_config_file, mock_loglevel, mock_config, mock_show_help
    ):
        sys.argv = [
            sys.argv[0],
            '--debug',
            '--config', 'config',
            'setup', 'account', 'configure',
            '--name', 'default',
            '--publish-settings-file', 'file',
            '--region', 'region',
            '--storage-account-name', 'storage',
            '--container-name', 'container'
        ]
        config_file = mock.Mock()
        mock_config_file.return_value = config_file
        mock_config.side_effect = AzureAccountLoadFailed('account-load-error')
        mock_show_help.return_value = False
        task = CliTask()
        task.load_config()
        config_file.default_new_config.assert_called_once_with()

    @patch('azurectl.cli_task.Cli.show_help')
    @patch('azurectl.cli_task.Config')
    @patch('azurectl.logger.log.setLevel')
    @raises(AzureAccountLoadFailed)
    def test_load_config_raises(
        self, mock_loglevel, mock_config, mock_show_help
    ):
        sys.argv = [
            sys.argv[0],
            '--debug',
            '--region', 'region',
            '--config', 'config',
            'compute', 'storage', 'container', 'list'
        ]
        mock_show_help.return_value = False
        mock_config.side_effect = AzureAccountLoadFailed('account-load-error')
        task = CliTask()
        task.load_config()
