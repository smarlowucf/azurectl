import sys
import mock
from nose.tools import *

import azure_cli
from azure_cli.disk_task import DiskTask

class TestDiskTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'disk', 'upload', 'image', 'container']
        self.task = DiskTask()
        azure_cli.disk_task.Disk = mock.Mock(
            return_value=mock.Mock()
        )
        azure_cli.disk_task.Container = mock.Mock(
            return_value=mock.Mock()
        )
        self.task.command_args = {}
        self.task.command_args['<container>'] = 'some-container'
        self.task.command_args['<image>'] = 'some-image'

    def test_process_upload(self):
        self.task.command_args['delete'] = False
        self.task.command_args['upload'] = True
        self.task.command_args['list']   = False
        self.task.process()
        self.task.disk.upload.assert_called_once_with(
            'some-image', None
        )

    def test_process_delete(self):
        self.task.command_args['delete'] = True
        self.task.command_args['upload'] = False
        self.task.command_args['list']   = False
        self.task.process()
        self.task.disk.delete.assert_called_once_with(
            'some-image'
        )

    def test_process_list(self):
        self.task.command_args['delete'] = False
        self.task.command_args['upload'] = False
        self.task.command_args['list']   = True
        self.task.process()
        self.task.container.content.assert_called_once_with(
            'some-container'
        )
