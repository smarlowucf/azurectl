import sys
import mock
from mock import patch


from test_helper import *

import azurectl
from azurectl.azurectl_exceptions import *
from azurectl.commands.compute_request import ComputeRequestTask


class TestComputeRequestTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'request', 'status', '--id', '1234'
        ]
        self.task = ComputeRequestTask()
        azurectl.commands.compute_request.RequestResult = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.commands.compute_request.Help = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.commands.compute_request.AzureAccount = mock.Mock(
            return_value=mock.Mock()
        )
        self.__init_command_args()

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['status'] = False
        self.task.command_args['wait'] = False
        self.task.command_args['--id'] = 1234
        self.task.command_args['help'] = False

    def test_process_compute_request_wait(self):
        self.__init_command_args()
        self.task.command_args['wait'] = True
        self.task.process()
        self.task.request_result.wait_for_request_completion.assert_called_once_with(
            self.task.service
        )

    @patch('azurectl.commands.compute_vm.DataOutput')
    def test_process_compute_request_status(self, mock_out):
        self.__init_command_args()
        self.task.command_args['status'] = True
        self.task.process()
        self.task.request_result.status.assert_called_once_with(
            self.task.service
        )

    def test_process_compute_request_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::request'
        )
