import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

import azurectl
from azurectl.setup_account_task import SetupAccountTask


class TestSetupAccountTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], 'setup', 'account', 'list'
        ]
        self.task = SetupAccountTask()
        azurectl.setup_account_task.AccountSetup = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.setup_account_task.Help = mock.Mock(
            return_value=mock.Mock()
        )

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['--color'] = False
        self.task.command_args['--name'] = 'foo'
        self.task.command_args['--publish-settings-file'] = 'file'
        self.task.command_args['--storage-account-name'] = 'foo'
        self.task.command_args['--container-name'] = 'foo'
        self.task.command_args['list'] = False
        self.task.command_args['add'] = False
        self.task.command_args['remove'] = False
        self.task.command_args['help'] = False

    @patch('azurectl.setup_account_task.DataOutput.display')
    @patch('azurectl.logger.log')
    def test_process_setup_account_list(self, mock_display, mock_logging):
        self.__init_command_args()
        self.task.command_args['list'] = True
        self.task.process()
        self.task.setup.list.assert_called_once_with()
        assert not mock_display.called
        mock_logging.info('There are no accounts configured')

    def test_process_setup_account_add(self):
        self.__init_command_args()
        self.task.command_args['add'] = True
        self.task.process()
        self.task.setup.add.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.command_args['--publish-settings-file'],
            self.task.command_args['--storage-account-name'],
            self.task.command_args['--container-name']
        )

    def test_process_setup_account_remove(self):
        self.__init_command_args()
        self.task.command_args['remove'] = True
        self.task.process()
        self.task.setup.remove.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_setup_account_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::setup::account'
        )
