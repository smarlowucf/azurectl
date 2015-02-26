import sys
import mock
from nose.tools import *

import azure_cli
from azure_cli.storage_task import StorageTask

class TestStorageTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'storage', 'list']
        self.task = StorageTask()
        azure_cli.storage_task.Storage = mock.Mock(
            return_value=mock.Mock()
        )

    def test_process_list(self):
        self.task.command_args['list'] = True
        self.task.process()
        self.task.storage.list.assert_called_once_with()
