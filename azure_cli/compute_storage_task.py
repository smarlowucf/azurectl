# Copyright (c) SUSE Linux GmbH.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
usage: azurectl compute storage account list
       azurectl compute storage container list
       azurectl compute storage container show
           [--container=<container>]
       azurectl compute storage upload <XZ-compressed-blob> <name>
           [--max-chunk-size=<size>]
           [--container=<container>]
       azurectl compute storage delete <name>
           [--container=<container>]

commands:
    account list    list storage account names
    container list  list container names for configured account
    container show  show container content for configured account and container
    upload          upload xz compressed blob to the given container
    delete          delete blob from the given container
"""
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
from storage import Storage
from container import Container


class ComputeStorageTask(CliTask):
    """
        Process storage commands
    """
    def process(self):
        self.account = AzureAccount(self.account_name, self.config_file)

        if self.command_args['--container']:
            container_name = self.command_args['--container']
        else:
            container_name = self.account.storage_container()

        self.storage = Storage(self.account, container_name)
        self.container = Container(self.account)

        if self.command_args['account'] and self.command_args['list']:
            self.__account_list()
        elif self.command_args['container'] and self.command_args['list']:
            self.__container_list()
        elif self.command_args['container'] and self.command_args['show']:
            self.__container_content(container_name)
        elif self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()
        else:
            raise AzureUnknownStorageCommand(self.command_args)

    def __upload(self):
        progress = BackgroundScheduler(timezone=utc)
        progress.add_job(
            self.storage.print_upload_status, 'interval', seconds=3
        )
        progress.start()
        try:
            image = self.command_args['<XZ-compressed-blob>']
            self.storage.upload(
                image, self.command_args['<name>'],
                self.command_args['--max-chunk-size']
            )
            self.storage.print_upload_status()
            progress.shutdown()
        except (KeyboardInterrupt):
            progress.shutdown()
        print
        Logger.info('Uploaded %s' % image)

    def __delete(self):
        image = self.command_args['<name>']
        self.storage.delete(image)
        Logger.info('Deleted %s' % image)

    def __container_content(self, container_name):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':container_content',
            self.container.content(container_name)
        )
        Logger.info(result.json(), 'Storage')

    def __container_list(self):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':containers',
            self.container.list()
        )
        Logger.info(result.json(), 'Storage')

    def __account_list(self):
        result = DataCollector()
        result.add('storage_names', self.account.storage_names())
        Logger.info(result.json(), 'Storage')
