import sys
import mock
from mock import patch
from nose.tools import *

import azure_cli
from azure_cli.container_task import ContainerTask


class TestContainerTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'container', 'list']
        self.task = ContainerTask()
        azure_cli.container_task.Container = mock.Mock(
            return_value=mock.Mock()
        )
        self.task.command_args = {}
        self.task.command_args['<name>'] = 'some-container-name'

    @patch('azure_cli.data_collector.json')
    def test_process_list(self, mock_json):
        self.task.command_args['list'] = True
        self.task.command_args['content'] = False
        self.task.process()
        self.task.container.list.assert_called_once_with()
