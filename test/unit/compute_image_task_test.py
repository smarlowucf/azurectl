import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

import azurectl
from azurectl.compute_image_task import ComputeImageTask


class TestComputeImageTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'image', 'list'
        ]
        self.task = ComputeImageTask()
        azurectl.compute_image_task.Image = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.compute_image_task.Help = mock.Mock(
            return_value=mock.Mock()
        )

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['--color'] = False
        self.task.command_args['list'] = False
        self.task.command_args['help'] = False

    @patch('azurectl.compute_image_task.DataOutput')
    def test_process_compute_image_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['list'] = True
        self.task.process()
        self.task.image.list.assert_called_once_with()

    def test_process_compute_image_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::image'
        )
