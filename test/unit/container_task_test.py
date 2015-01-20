import mock
from nose.tools import *

import azure_cli
from azure_cli.container_task import ContainerTask

class FakeContainerCommand:
    def Container(self, account):
        pass


class TestContainerTask:
    def setup(self):
        self.task = ContainerTask()
        self.task.azure = mock.Mock(
            return_value=FakeContainerCommand()
        )
        self.task.command_args = {}
        self.task.command_args['<name>'] = 'some-container-name'

    def test_process(self):
        self.task.command_args['list'] = True
        self.task.command_args['content'] = False
        self.task.process()
