import sys
import mock
from nose.tools import *

import azure_cli
from azure_cli.compute_help_task import ComputeHelpTask


class TestComputeHelpTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'compute', 'help', '--command', 'foo']
        self.task = ComputeHelpTask()
        azure_cli.compute_help_task.Help = mock.Mock(
            return_value=mock.Mock()
        )

    def test_process_compute_help(self):
        self.task.process()
        self.task.help.show.assert_called_once_with('foo')
