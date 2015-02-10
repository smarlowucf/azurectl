import mock
from nose.tools import *

import azure_cli
from azure_cli.image_task import ImageTask

class TestImageTask:
    def setup(self):
        self.task = ImageTask()
        azure_cli.image_task.Image = mock.Mock(
            return_value=mock.Mock()
        )
        self.task.command_args = {}
        self.task.command_args['list'] = True

    def test_process(self):
        self.task.process()
        self.task.image.list.assert_called_once_with()
