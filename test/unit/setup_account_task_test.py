import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

import azurectl
from azurectl.azurectl_exceptions import *
from azurectl.setup_account_task import SetupAccountTask


class TestSetupAccountTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'setup', 'account', 'list'
        ]
        self.setup = mock.Mock()
        self.setup.list = mock.Mock(
            return_value=['a', 'b']
        )
        azurectl.setup_account_task.AccountSetup = mock.Mock(
            return_value=self.setup
        )
        azurectl.setup_account_task.Help = mock.Mock(
            return_value=mock.Mock()
        )
        self.task = SetupAccountTask()

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['--color'] = False
        self.task.command_args['--name'] = 'foo'
        self.task.command_args['--publish-settings-file'] = 'file'
        self.task.command_args['--storage-account-name'] = 'foo'
        self.task.command_args['--container-name'] = 'foo'
        self.task.command_args['--subscription-id'] = False
        self.task.command_args['--region'] = 'region'
        self.task.command_args['list'] = False
        self.task.command_args['add'] = False
        self.task.command_args['configure'] = False
        self.task.command_args['region'] = False
        self.task.command_args['remove'] = False
        self.task.command_args['default'] = False
        self.task.command_args['help'] = False

    @patch('azurectl.setup_account_task.DataOutput.display')
    @patch('azurectl.logger.log')
    def test_process_setup_account_list(self, mock_display, mock_logging):
        self.__init_command_args()
        self.task.command_args['list'] = True
        self.task.process()
        self.task.setup.list.assert_called_once_with()

    @patch('azurectl.logger.log.info')
    def test_process_setup_account_list_empty(self, mock_info):
        self.__init_command_args()
        self.task.command_args['list'] = True
        self.setup.list.return_value = None
        self.task.process()
        mock_info.assert_called_once_with(
            'There are no accounts configured'
        )

    def test_process_setup_account_add(self):
        self.__init_command_args()
        self.task.command_args['add'] = True
        self.task.process()
        self.task.setup.add_account.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.command_args['--publish-settings-file'],
            False
        )

    def test_process_setup_account_add_with_subscription_id(self):
        self.__init_command_args()
        self.task.command_args['add'] = True
        self.task.command_args['--subscription-id'] = '1234'
        self.task.process()
        self.task.setup.add_account.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.command_args['--publish-settings-file'],
            self.task.command_args['--subscription-id']
        )

    def test_process_setup_region_add(self):
        self.__init_command_args()
        self.task.command_args['add'] = True
        self.task.command_args['region'] = True
        self.task.process()
        self.task.setup.add_region.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.command_args['--storage-account-name'][0],
            self.task.command_args['--container-name'][0],
            self.task.command_args['--storage-account-name'],
            self.task.command_args['--container-name']
        )

    def test_process_setup_configure_account_and_region(self):
        self.__init_command_args()
        self.task.command_args['configure'] = True
        self.task.process()
        self.task.setup.configure_account_and_region.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.command_args['--publish-settings-file'],
            self.task.command_args['--region'],
            self.task.command_args['--storage-account-name'][0],
            self.task.command_args['--container-name'][0],
            self.task.command_args['--storage-account-name'],
            self.task.command_args['--container-name'],
            self.task.command_args['--subscription-id']
        )

    def test_process_setup_account_remove(self):
        self.__init_command_args()
        self.task.command_args['remove'] = True
        self.task.process()
        self.task.setup.remove.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_setup_default_account(self):
        self.__init_command_args()
        self.task.command_args['default'] = True
        self.task.process()
        self.task.setup.set_default_account.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_setup_default_region(self):
        self.__init_command_args()
        self.task.command_args['default'] = True
        self.task.command_args['region'] = True
        self.task.process()
        self.task.setup.set_default_region.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_setup_account_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::setup::account'
        )

    def test_process_setup_account_configure_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['configure'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::setup::account::configure'
        )

    def test_process_setup_account_region_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['region'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::setup::account::region'
        )
