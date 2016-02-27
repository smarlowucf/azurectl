import sys
import mock
from nose.tools import *
from mock import patch

import logging

import nose_helper

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
    @patch('azurectl.cli_task.Config')
    @patch('azurectl.logger.log.setLevel')
    def test_cli_init(
        self, mock_loglevel, mock_config, mock_show_help,
    ):
        sys.argv = [
            sys.argv[0],
            '--debug',
            '--region', 'region',
            '--config', 'config',
            'compute', 'storage', 'account', 'list'
        ]
        mock_show_help.return_value = False
        task = CliTask()
        mock_config.assert_called_once_with(
            None, 'region', None, None, 'config'
        )
        mock_loglevel.assert_called_once_with(logging.DEBUG)

    @patch('azurectl.cli_task.Validations.validate_min_length')
    def test_validate_min_length(self, mock_validation):
        sys.argv = [
            sys.argv[0],
            '--config', 'config',
            'setup', 'account', 'default', '--name', 'test-name0'
        ]
        task = CliTask(should_load_config=False)
        task.validate_min_length('--name', 5)
        mock_validation.assert_called_once_with('--name', 'test-name0', 5)

    @patch('azurectl.cli_task.Validations.validate_max_length')
    def test_validate_max_length(self, mock_validation):
        sys.argv = [
            sys.argv[0],
            '--config', 'config',
            'setup', 'account', 'default', '--name', 'test-name0'
        ]
        task = CliTask(should_load_config=False)
        task.validate_max_length('--name', 10)
        mock_validation.assert_called_once_with('--name', 'test-name0', 10)
