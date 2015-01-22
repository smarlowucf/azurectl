import mock
from nose.tools import *

import azure_cli
from azure_cli.disk_task import DiskTask

class FakeDiskCommand:
    def Disk(self, account, container):
        pass


class TestDiskTask:
    def setup(self):
        self.task = DiskTask()
        self.task.azure = mock.Mock(
            return_value=FakeDiskCommand()
        )
        self.task.command_args = {}
        self.task.command_args['<container>'] = 'some-container'
        self.task.command_args['<image>'] = 'some-image'

    def test_process_upload(self):
        self.task.command_args['delete'] = False
        self.task.command_args['upload'] = True
        self.task.process()
        self.task.disk.upload.assert_called_once_with(
            'some-image', None, None
        )

    def test_process_delete(self):
        self.task.command_args['delete'] = True
        self.task.command_args['upload'] = False
        self.task.process()
        self.task.disk.delete.assert_called_once_with(
            'some-image'
        )
