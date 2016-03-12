import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

import azurectl
from azurectl.compute_data_disk_task import ComputeDataDiskTask
from azurectl.azurectl_exceptions import *


class TestComputeDataDiskTask:
    def setup(self):
        # instantiate the command task
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'data-disk', 'help'
        ]
        self.task = ComputeDataDiskTask()
        # mock out the DataDisk class the commands interface with
        azurectl.compute_data_disk_task.DataDisk = mock.Mock(
            return_value=mock.Mock()
        )
        # mock out the help class
        azurectl.compute_data_disk_task.Help = mock.Mock(
            return_value=mock.Mock()
        )
        # mock out the output class
        azurectl.compute_data_disk_task.DataOutput = mock.Mock(
            return_value=mock.Mock()
        )
        # variables used in multiple tests
        self.cloud_service_name = 'mockcloudservice'
        self.instance_name = 'mockcloudserviceinstance1'
        self.lun = 0
        self.cache_method = 'ReadWrite'
        self.disk_filename = 'mockcloudserviceinstance1-data-disk-0.vhd'
        self.disk_url = ('https://foo/bar/' + self.disk_filename)
        self.disk_label = 'Mock data disk'
        self.disk_size = 42

    def __init_command_args(self, overrides=None):
        '''
            Provide an empty set of command arguments to be customized in tests
        '''
        command_args = {
            'create': False,
            'delete': False,
            'show': False,
            'help': False,
            '--cloud-service-name': None,
            '--size': None,
            '--instance-name': None,
            '--label': None,
            '--disk-name': None,
            '--lun': None,
            '--no-cache': False,
            '--read-only-cache': False,
            '--read-write-cache': False
        }
        if overrides:
            command_args.update(overrides)
        self.task.command_args = command_args

    def test_help(self):
        # given
        self.__init_command_args({
            'help': True
        })
        # when
        self.task.process()
        # then
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::data_disk'
        )

    def test_create_with_minimal_args(self):
        # given
        self.__init_command_args({
            'create': True,
            '--cloud-service-name': self.cloud_service_name,
            '--size': self.disk_size
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.create.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.disk_size
        )

    def test_create_with_instance_name(self):
        # given
        self.__init_command_args({
            'create': True,
            '--cloud-service-name': self.cloud_service_name,
            '--instance-name': self.instance_name,
            '--size': self.disk_size
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.create.assert_called_once_with(
            self.cloud_service_name,
            self.instance_name,
            self.disk_size
        )

    def test_create_with_optional_args(self):
        # given
        self.__init_command_args({
            'create': True,
            '--cloud-service-name': self.cloud_service_name,
            '--instance-name': self.instance_name,
            '--size': self.disk_size,
            '--label': self.disk_label,
            '--disk-name': self.disk_filename,
            '--lun': str(self.lun)
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.create.assert_called_once_with(
            self.cloud_service_name,
            self.instance_name,
            self.disk_size,
            label=self.disk_label,
            filename=self.disk_filename,
            lun=self.lun
        )

    def test_create_with_cache_method(self):
        sets = [
            ['--no-cache', 'None'],
            ['--read-only-cache', 'ReadOnly'],
            ['--read-write-cache', 'ReadWrite']
        ]
        for cache_method_arg, host_caching in sets:
            self.check_create_with_cache_method(cache_method_arg, host_caching)

    def check_create_with_cache_method(self, cache_method_arg, host_caching):
        # given
        self.__init_command_args({
            'create': True,
            '--cloud-service-name': self.cloud_service_name,
            '--size': self.disk_size
        })
        self.task.command_args[cache_method_arg] = True
        # when
        self.task.process()
        # then
        self.task.data_disk.create.assert_called_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.disk_size,
            host_caching=host_caching
        )

    def test_show_with_minimal_args(self):
        # given
        self.__init_command_args({
            'show': True,
            '--cloud-service-name': self.cloud_service_name,
            '--lun': self.lun
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.show.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.lun
        )

    def test_show_with_instance_name(self):
        # given
        self.__init_command_args({
            'show': True,
            '--cloud-service-name': self.cloud_service_name,
            '--instance-name': self.instance_name,
            '--lun': self.lun
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.show.assert_called_once_with(
            self.cloud_service_name,
            self.instance_name,
            self.lun
        )

    def test_delete_with_minimal_args(self):
        # given
        self.__init_command_args({
            'delete': True,
            '--cloud-service-name': self.cloud_service_name,
            '--lun': self.lun
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.delete.assert_called_once_with(
            self.cloud_service_name,
            self.cloud_service_name,
            self.lun
        )

    def test_delete_with_instance_name(self):
        # given
        self.__init_command_args({
            'delete': True,
            '--cloud-service-name': self.cloud_service_name,
            '--instance-name': self.instance_name,
            '--lun': self.lun
        })
        # when
        self.task.process()
        # then
        self.task.data_disk.delete.assert_called_once_with(
            self.cloud_service_name,
            self.instance_name,
            self.lun
        )
