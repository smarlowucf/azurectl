import sys
import mock
from mock import patch
from nose.tools import *

import azure_cli
from azure_cli.compute_storage_task import ComputeStorageTask


class TestComputeStorageTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], 'compute', 'storage', 'upload', 'blob', 'name'
        ]
        self.task = ComputeStorageTask()
        azure_cli.compute_storage_task.AzureAccount.storage_names = mock.Mock(
            return_value=mock.Mock()
        )
        azure_cli.compute_storage_task.Storage = mock.Mock(
            return_value=mock.Mock()
        )
        azure_cli.compute_storage_task.Container = mock.Mock(
            return_value=mock.Mock()
        )
        self.__init_command_args()

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['container'] = False
        self.task.command_args['account'] = False
        self.task.command_args['delete'] = False
        self.task.command_args['upload'] = False
        self.task.command_args['list'] = False
        self.task.command_args['show'] = False
        self.task.command_args['--container'] = 'some-container'
        self.task.command_args['<XZ-compressed-blob>'] = 'some-file'
        self.task.command_args['--max-chunk-size'] = 1024
        self.task.command_args['<name>'] = 'some-blob'

    @patch('azure_cli.data_collector.json')
    def test_process_compute_storage_account_list(self, mock_json):
        self.__init_command_args()
        self.task.command_args['account'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.account.storage_names.assert_called_once_with()

    @patch('azure_cli.data_collector.json')
    def test_process_compute_storage_show(self, mock_json):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['show'] = True
        self.task.process()
        self.task.container.content.assert_called_once_with(
            'some-container'
        )

    @patch('azure_cli.data_collector.json')
    def test_process_compute_storage_list(self, mock_json):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.container.list.assert_called_once_with()

    def test_process_compute_storage_upload(self):
        self.__init_command_args()
        self.task.command_args['upload'] = True
        self.task.process()
        self.task.storage.upload.assert_called_once_with(
            'some-file', 'some-blob', 1024
        )

    def test_process_compute_storage_delete(self):
        self.__init_command_args()
        self.task.command_args['delete'] = True
        self.task.process()
        self.task.storage.delete.assert_called_once_with(
            'some-blob'
        )
