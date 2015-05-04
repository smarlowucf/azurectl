# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
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
usage: azurectl compute storage -h | --help
       azurectl compute storage account list
       azurectl compute storage container list
       azurectl compute storage container show
           [--container=<container>]
       azurectl compute storage container sas
           [--container=<container>]
           [--start-datetime=<start>]
           [--expiry-datetime=<expiry>]
           [--permissions=<permissions>]
       azurectl compute storage upload --source=<xzfile> --name=<blobname>
           [--max-chunk-size=<size>]
           [--container=<container>]
           [--quiet]
       azurectl compute storage delete --name=<blobname>
           [--container=<container>]
       azurectl compute storage account help
       azurectl compute storage container help
       azurectl compute storage help

commands:
    account list
        list storage account names
    container list
        list storage container names for configured account
    container show
        show container content for configured account and container
    upload
        upload xz compressed blob to the given container
    delete
        delete blob from the given container
    --source=<xzfile>
        XZ compressed data file
    --name=<name>
        name of the file in the storage pool
    --max-chunk-size=<size>
        max chunk size in bytes for upload, default 4MB
    --container=<container>
        container name, overwrites configuration value
    --start-datetime=<start>
        Date (and optionally time) to grant access via a shared access
        signature. [default: now]
    --expiry-datetime=<start>
        Date (and optionally time) to cease access via a shared access
        signature. [default: 30 days from start]
    --permissions=<permissions>
        String of permitted actions on a storage element via shared access
        signature.
        r  Read
        w  Write
        d  Delete
        l  List
        [default: rl]
    --quiet
        suppress progress information on upload
    account help
        show manual page for account sub command
    container help
        show manual page for container sub command
    help
        show manual page for storage command
"""
import datetime
import dateutil.parser
import re
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
from help import Help


class ComputeStorageTask(CliTask):
    """
        Process storage commands
    """
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.account = AzureAccount(self.account_name, self.config_file)

        if self.command_args['--container']:
            container_name = self.command_args['--container']
        else:
            container_name = self.account.storage_container()

        # default to 1 minute ago (skew around 'now')
        if self.command_args['--start-datetime'] == 'now':
            start = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
        else:
            start = self.__validate_date_arg('--start-datetime')

        # default to 30 days from now
        if self.command_args['--expiry-datetime'] == '30 days from start':
            expiry = start + datetime.timedelta(days=30)
        else:
            expiry = self.__validate_date_arg('--expiry-datetime')

        self.__validate_permissions_arg()

        self.storage = Storage(self.account, container_name)
        self.container = Container(self.account)

        if self.command_args['account'] and self.command_args['list']:
            self.__account_list()
        elif self.command_args['container'] and self.command_args['list']:
            self.__container_list()
        elif self.command_args['container'] and self.command_args['show']:
            self.__container_content(container_name)
        elif self.command_args['container'] and self.command_args['sas']:
            self.__container_sas(
                container_name,
                start,
                expiry,
                self.command_args['--permissions']
            )
        elif self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()
        else:
            raise AzureUnknownCommand(self.command_args)

    # argument validation

    def __validate_date_arg(self, cmd_arg):
        try:
            date = dateutil.parser.parse(self.command_args[cmd_arg])
            return date
        except ValueError:
            raise AzureInvalidCommand(
                cmd_arg + '=' + self.command_args[cmd_arg]
            )

    def __validate_permissions_arg(self):
        if (not re.match("^([rwld]+)$", self.command_args['--permissions'])):
            raise AzureInvalidCommand(
                '--permissions=' + self.command_args['--permissions']
            )

    # tasks

    def __help(self):
        if self.command_args['account'] and self.command_args['help']:
            self.manual.show('azurectl::compute::storage::account')
        elif self.command_args['container'] and self.command_args['help']:
            self.manual.show('azurectl::compute::storage::container')
        elif self.command_args['help']:
            self.manual.show('azurectl::compute::storage')
        else:
            return False
        return self.manual

    def __upload(self):
        if self.command_args['--quiet']:
            self.__upload_no_progress()
        else:
            self.__upload_with_progress()

    def __upload_no_progress(self):
        try:
            self.__process_upload()
        except (KeyboardInterrupt):
            progress.shutdown()

    def __upload_with_progress(self):
        image = self.command_args['--source']
        progress = BackgroundScheduler(timezone=utc)
        progress.add_job(
            self.storage.print_upload_status, 'interval', seconds=3
        )
        progress.start()
        try:
            self.__process_upload()
            self.storage.print_upload_status()
            progress.shutdown()
        except (KeyboardInterrupt):
            progress.shutdown()
        print
        Logger.info('Uploaded %s' % image)

    def __process_upload(self):
        self.storage.upload(
            self.command_args['--source'],
            self.command_args['--name'],
            self.command_args['--max-chunk-size']
        )

    def __delete(self):
        image = self.command_args['--name']
        self.storage.delete(image)
        Logger.info('Deleted %s' % image)

    def __container_sas(self, container_name, start, expiry, permissions):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':container_sas_url',
            self.container.sas(container_name, start, expiry, permissions)
        )
        Logger.info(result.json(), 'Storage')

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
