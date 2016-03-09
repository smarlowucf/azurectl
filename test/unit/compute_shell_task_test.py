import sys
import mock
from collections import namedtuple
from mock import patch
from nose.tools import *

import nose_helper

import azurectl
from azurectl.azure_account import AzureAccount
from azurectl.compute_shell_task import ComputeShellTask
from azurectl.config import Config


class TestComputeShellTask:
    def setup(self):
        sys.argv = [
            sys.argv[0], '--config', '../data/config',
            'compute', 'shell'
        ]

        account = AzureAccount(
            Config(
                region_name='East US 2', filename='../data/config'
            )
        )
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id', 'management_url']
        )
        account.publishsettings = mock.Mock(
            return_value=credentials(
                private_key='abc',
                certificate='abc',
                subscription_id='4711',
                management_url='test.url'
            )
        )
        account.get_blob_service_host_base = mock.Mock(
            return_value='.blob.test.url'
        )
        account.storage_key = mock.Mock()

        azurectl.compute_shell_task.AzureAccount = mock.Mock(
            return_value=account
        )

        self.task = ComputeShellTask()

    @patch('azurectl.compute_shell_task.code.interact')
    def test_process_compute_shell(self, mock_interact):
        self.task.command_args = {}
        self.task.process()
        mock_interact.assert_called_once_with(local={
            'service': self.task.service
        })
