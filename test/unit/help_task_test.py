import mock
from nose.tools import *

import azure_cli
from azure_cli.help_task import HelpTask

class FakeHelpCommand:
    def Help(self, account):
        pass


class TestHelpTask:
    def setup(self):
        self.task = HelpTask()
        self.task.azure = mock.Mock(
            return_value=FakeHelpCommand()
        )

    def test_process(self):
        self.task.process()
        self.task.azure.Help.assert_called_once_with()
