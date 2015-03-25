import sys
import mock
from mock import patch
from nose.tools import *

import azure_cli
from azure_cli.image_task import ImageTask


class TestImageTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'image', 'list']

        self.task = ImageTask()
        azure_cli.image_task.Image = mock.Mock(
            return_value=mock.Mock()
        )
        self.task.command_args = {}
        self.task.command_args['list'] = True

    @patch('azure_cli.data_collector.json')
    def test_process(self, mock_json):
        self.task.process()
        self.task.image.list.assert_called_once_with()
