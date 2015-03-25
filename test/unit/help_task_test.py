import sys
import mock
from nose.tools import *

import azure_cli
from azure_cli.help_task import HelpTask


class TestHelpTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'help', 'command']
        self.task = HelpTask()
        azure_cli.help_task.Help = mock.Mock(
            return_value=mock.Mock()
        )
        self.task.command_args['<command>'] = 'help-for-foo'

    def test_process(self):
        self.task.process()
        self.task.help.show.assert_called_once_with('help-for-foo')
