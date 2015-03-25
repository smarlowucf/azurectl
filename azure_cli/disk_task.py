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
usage: azurectl disk upload <XZ-compressed-image> <name>
           [--max-chunk-size=<size>]
           [--container=<container>]
       azurectl disk delete <name>
           [--container=<container>]
       azurectl disk list
           [--container=<container>]

commands:
    upload   upload image to the given container
    delete   delete image in the given container
    list     list content of given container for configured storage account

options:
    --max-chunk-size=<size>  max chunk byte size for disk upload
    --container=<container>  set container name to use for the operation
"""
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
from disk import Disk
from container import Container


class DiskTask(CliTask):
    """
        Process disk command
    """
    def process(self):
        self.account = AzureAccount(self.account_name, self.config_file)
        container_name = None
        if self.command_args['--container']:
            container_name = self.command_args['--container']
        else:
            container_name = self.account.storage_container()
        self.disk = Disk(self.account, container_name)
        self.container = Container(self.account)
        if self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()
        elif self.command_args['list']:
            self.__list(container_name)
        else:
            raise AzureUnknownDiskCommand(self.command_args)

    def __upload(self):
        progress = BackgroundScheduler(timezone=utc)
        progress.add_job(
            self.disk.print_upload_status, 'interval', seconds=3
        )
        progress.start()
        try:
            image = self.command_args['<XZ-compressed-image>']
            self.disk.upload(
                image, self.command_args['<name>'],
                self.command_args['--max-chunk-size']
            )
            self.disk.print_upload_status()
            progress.shutdown()
        except (KeyboardInterrupt):
            progress.shutdown()
        print
        Logger.info('Uploaded %s' % image)

    def __delete(self):
        image = self.command_args['<name>']
        self.disk.delete(image)
        Logger.info('Deleted %s' % image)

    def __list(self, container_name):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':container_content',
            self.container.content(container_name)
        )
        Logger.info(result.json(), 'Disk')
