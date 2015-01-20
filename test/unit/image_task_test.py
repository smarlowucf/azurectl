import mock
from nose.tools import *

import azure_cli
from azure_cli.image_task import ImageTask

class FakeImageCommand:
    def Image(self, account):
        pass


class TestImageTask:
    def setup(self):
        self.task = ImageTask()
        self.task.azure = mock.Mock(
            return_value=FakeImageCommand()
        )
        self.task.command_args = {}
        self.task.command_args['list'] = True

    def test_process(self):
        self.task.process()
