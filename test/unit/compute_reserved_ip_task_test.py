import sys
import mock
from mock import patch


from test_helper import *

import azurectl
from azurectl.compute_reserved_ip_task import ComputeReservedIpTask
from azurectl.azurectl_exceptions import *


class TestComputeReservedIpTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'reserved-ip', 'list'
        ]
        self.task = ComputeReservedIpTask()
        azurectl.compute_reserved_ip_task.ReservedIp = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.compute_reserved_ip_task.Help = mock.Mock(
            return_value=mock.Mock()
        )

    def __init_command_args(self):
        self.task.command_args = {
            'list': False,
            'show': False,
            'create': False,
            'delete': False,
            'help': False,
            '--name': None
        }

    def test_process_compute_reserved_ip_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::reserved_ip'
        )

    @patch('azurectl.compute_reserved_ip_task.DataOutput')
    def test_process_compute_reserved_ip_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['list'] = True
        self.task.process()
        self.task.reserved_ip.list.assert_called_once_with()

    @patch('azurectl.compute_reserved_ip_task.DataOutput')
    def test_process_compute_reserved_ip_show(self, mock_out):
        self.__init_command_args()
        self.task.command_args['show'] = True
        self.task.command_args['--name'] = 'test'
        self.task.process()
        self.task.reserved_ip.show.assert_called_once_with(
            self.task.command_args['--name']
        )

    @patch('azurectl.compute_reserved_ip_task.DataOutput')
    def test_process_compute_reserved_ip_create(self, mock_out):
        self.__init_command_args()
        self.task.command_args['create'] = True
        self.task.command_args['--name'] = 'test'
        self.task.process()
        self.task.reserved_ip.create.assert_called_once_with(
            self.task.command_args['--name'],
            self.task.config.get_region_name()
        )

    @patch('azurectl.compute_reserved_ip_task.DataOutput')
    def test_process_compute_reserved_ip_delete(self, mock_out):
        self.__init_command_args()
        self.task.command_args['delete'] = True
        self.task.command_args['--name'] = 'test'
        self.task.process()
        self.task.reserved_ip.delete.assert_called_once_with(
            self.task.command_args['--name']
        )
