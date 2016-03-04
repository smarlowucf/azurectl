import dateutil.parser
import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

import datetime
import azurectl
from azurectl.azurectl_exceptions import *
from azurectl.compute_storage_task import ComputeStorageTask


class TestComputeStorageTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'storage', 'upload',
            '--source', 'blob',
            '--name', 'name'
        ]
        azurectl.compute_storage_task.AzureAccount.storage_names = mock.Mock(
            return_value=mock.Mock()
        )
        self.storage = mock.Mock()
        self.storage.upload = mock.Mock()
        azurectl.compute_storage_task.Storage = mock.Mock(
            return_value=self.storage
        )
        azurectl.compute_storage_task.Container = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.compute_storage_task.FileShare = mock.Mock(
            return_value=mock.Mock()
        )
        azurectl.compute_storage_task.Help = mock.Mock(
            return_value=mock.Mock()
        )
        self.task = ComputeStorageTask()
        self.__init_command_args()

    def __init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['share'] = False
        self.task.command_args['create'] = False
        self.task.command_args['container'] = False
        self.task.command_args['account'] = False
        self.task.command_args['delete'] = False
        self.task.command_args['upload'] = False
        self.task.command_args['list'] = False
        self.task.command_args['show'] = False
        self.task.command_args['sas'] = False
        self.task.command_args['--color'] = False
        self.task.command_args['--start-datetime'] = '2015-01-01'
        self.task.command_args['--expiry-datetime'] = '2015-12-31'
        self.task.command_args['--permissions'] = 'rl'
        self.task.command_args['--source'] = 'some-file'
        self.task.command_args['--max-chunk-size'] = 1024
        self.task.command_args['--quiet'] = False
        self.task.command_args['--name'] = 'some-name'
        self.task.command_args['help'] = False

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_share_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['share'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.fileshare.list.assert_called_once_with()

    def test_process_compute_storage_container_delete(self):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['delete'] = True
        self.task.process()
        self.task.container.delete.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_compute_storage_container_create(self):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['create'] = True
        self.task.process()
        self.task.container.create.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_compute_storage_share_delete(self):
        self.__init_command_args()
        self.task.command_args['share'] = True
        self.task.command_args['delete'] = True
        self.task.process()
        self.task.fileshare.delete.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_compute_storage_share_create(self):
        self.__init_command_args()
        self.task.command_args['share'] = True
        self.task.command_args['create'] = True
        self.task.process()
        self.task.fileshare.create.assert_called_once_with(
            self.task.command_args['--name']
        )

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_account_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['account'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.account.storage_names.assert_called_once_with()

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_show(self, mock_out):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['show'] = True
        self.task.process()
        self.task.container.content.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_start_date_validation(self):
        self.__init_command_args()
        self.task.command_args['--start-datetime'] = 'foo'
        assert_raises(AzureInvalidCommand, self.task.process)

    def test_end_date_validation(self):
        self.__init_command_args()
        self.task.command_args['--expiry-datetime'] = 'foo'
        assert_raises(AzureInvalidCommand, self.task.process)

    def test_permissions_validation(self):
        self.__init_command_args()
        self.task.command_args['--permissions'] = 'a'
        assert_raises(AzureInvalidCommand, self.task.process)

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_container_sas(self, mock_out):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['sas'] = True
        self.task.process()
        start = dateutil.parser.parse(
            self.task.command_args['--start-datetime']
        )
        expiry = dateutil.parser.parse(
            self.task.command_args['--expiry-datetime']
        )
        self.task.container.sas.assert_called_once_with(
            self.task.command_args['--name'], start, expiry, 'rl'
        )

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_container_sas_now(self, mock_out):
        self.__init_command_args()
        self.task.command_args['--start-datetime'] = 'now'
        self.task.command_args['container'] = True
        self.task.command_args['sas'] = True
        self.task.process()
        expiry = dateutil.parser.parse(
            self.task.command_args['--expiry-datetime']
        )
        self.task.container.sas.assert_called_once_with(
            self.task.command_args['--name'], mock.ANY, expiry, 'rl'
        )

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_container_sas_expire(self, mock_out):
        self.__init_command_args()
        self.task.command_args['--expiry-datetime'] = '30 days from start'
        self.task.command_args['container'] = True
        self.task.command_args['sas'] = True
        self.task.process()
        start = dateutil.parser.parse(
            self.task.command_args['--start-datetime']
        )
        expiry = start + datetime.timedelta(days=30)
        self.task.container.sas.assert_called_once_with(
            self.task.command_args['--name'], start, expiry, 'rl'
        )

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_container_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.container.list.assert_called_once_with()

    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_container_from_cfg_list(self, mock_out):
        self.__init_command_args()
        self.task.command_args['container'] = True
        self.task.command_args['list'] = True
        self.task.process()
        self.task.container.list.assert_called_once_with()

    @patch('azurectl.compute_storage_task.BackgroundScheduler')
    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_upload(self, mock_out, mock_job):
        self.__init_command_args()
        self.task.command_args['upload'] = True
        self.task.process()
        self.task.storage.upload.assert_called_once_with(
            'some-file', self.task.command_args['--name'], 1024
        )

    @raises(SystemExit)
    @patch('azurectl.compute_storage_task.BackgroundScheduler')
    @patch('azurectl.compute_storage_task.DataOutput')
    def test_process_compute_storage_upload_interrupted(self, mock_out, mock_job):
        self.__init_command_args()
        self.task.command_args['upload'] = True
        self.storage.upload.side_effect = KeyboardInterrupt
        self.task.process()

    @raises(SystemExit)
    @patch('azurectl.compute_storage_task.BackgroundScheduler')
    def test_process_compute_storage_upload_quiet_interrupted(self, mock_job):
        self.__init_command_args()
        self.task.command_args['upload'] = True
        self.task.command_args['--quiet'] = True
        self.storage.upload.side_effect = KeyboardInterrupt
        self.task.process()

    def test_process_compute_storage_delete(self):
        self.__init_command_args()
        self.task.command_args['delete'] = True
        self.task.process()
        self.task.storage.delete.assert_called_once_with(
            self.task.command_args['--name']
        )

    def test_process_compute_storage_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::storage'
        )

    def test_process_compute_storage_account_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['account'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::storage::account'
        )

    def test_process_compute_storage_container_help(self):
        self.__init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['container'] = True
        self.task.process()
        self.task.manual.show.assert_called_once_with(
            'azurectl::compute::storage::container'
        )
