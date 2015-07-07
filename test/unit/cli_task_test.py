import sys
import mock
from nose.tools import *
from mock import patch

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

    @patch('os.path.isfile')
    @patch('ConfigParser.ConfigParser.has_section')
    def test_global_args(self, mock_section, mock_isfile):
        sys.argv = [
            sys.argv[0], '--account', 'account', '--config', 'config',
            'compute', 'storage', 'account', 'list'
        ]
        task = CliTask()
        assert task.account_name == 'account'
        assert task.config_file == 'config'
