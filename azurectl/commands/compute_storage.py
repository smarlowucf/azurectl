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
       azurectl compute storage container list
       azurectl compute storage container show
           [--name=<containername>]
       azurectl compute storage container create
           [--name=<containername>]
       azurectl compute storage container delete --name=<containername>
       azurectl compute storage container sas
           [--name=<containername>]
           [--start-datetime=<start>]
           [--expiry-datetime=<expiry>]
           [--permissions=<permissions>]
       azurectl compute storage share list
       azurectl compute storage share create --name=<sharename>
       azurectl compute storage share delete --name=<sharename>
       azurectl compute storage upload --source=<file>
           [--name=<blobname>]
           [--max-chunk-size=<size>]
           [--quiet]
       azurectl compute storage delete --name=<blobname>
       azurectl compute storage container help
       azurectl compute storage share help
       azurectl compute storage help

commands:
    container list
        list storage container names for configured account
    container show
        show container content for configured account and container
    container create
        create container with the specified name
    container delete
        delete container with the specified name
    upload
        upload xz compressed blob to the given container
    delete
        storage: delete blob from the given container
        storage share: delete share from the storage account
    create
        create file share in the storage account
    container help
        show manual page for container sub command
    share help
        show manual page for share sub command
    help
        show manual page for storage command

options:
    --source=<file>
        file to upload
    --name=<name>
        blobname: name of the file in the storage pool
        sharename: name of the files share
        containername: name of the container
    --max-chunk-size=<size>
        max chunk size in bytes for upload, default 4MB
    --start-datetime=<start>
        Date (and optionally time) to grant access via a shared access
        signature. [default: now]
    --expiry-datetime=<expiry>
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
"""
import datetime
import dateutil.parser
import re
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

# project
from base import CliTask
from ..account.service import AzureAccount
from ..utils.collector import DataCollector
from ..utils.output import DataOutput
from ..logger import log
from ..azurectl_exceptions import AzureInvalidCommand
from ..storage.storage import Storage
from ..storage.container import Container
from ..storage.fileshare import FileShare
from ..help import Help


class ComputeStorageTask(CliTask):
    """
        Process storage commands
    """
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.result = DataCollector()
        self.out = DataOutput(
            self.result,
            self.global_args['--output-format'],
            self.global_args['--output-style']
        )

        self.load_config()

        self.account = AzureAccount(self.config)

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
        self.fileshare = FileShare(self.account)

        if self.command_args['container'] and self.command_args['list']:
            self.__container_list()
        elif self.command_args['container'] and self.command_args['show']:
            self.__container_content(container_name)
        elif self.command_args['container'] and self.command_args['create']:
            self.__container_create(container_name)
        elif self.command_args['container'] and self.command_args['delete']:
            self.__container_delete(container_name)
        elif self.command_args['container'] and self.command_args['sas']:
            self.__container_sas(
                container_name,
                start,
                expiry,
                self.command_args['--permissions']
            )
        elif self.command_args['share'] and self.command_args['list']:
            self.__share_list()
        elif self.command_args['share'] and self.command_args['create']:
            self.__share_create()
        elif self.command_args['share'] and self.command_args['delete']:
            self.__share_delete()
        elif self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()

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
        if self.command_args['container'] and self.command_args['help']:
            self.manual.show('azurectl::compute::storage::container')
        elif self.command_args['share'] and self.command_args['help']:
            self.manual.show('azurectl::compute::storage::share')
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
            raise SystemExit('azurectl aborted by keyboard interrupt')

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
            raise SystemExit('azurectl aborted by keyboard interrupt')
        print
        log.info('Uploaded %s', image)

    def __process_upload(self):
        self.storage.upload(
            self.command_args['--source'],
            self.command_args['--name'],
            self.command_args['--max-chunk-size']
        )

    def __delete(self):
        image = self.command_args['--name']
        self.storage.delete(image)
        log.info('Deleted %s', image)

    def __container_sas(self, container_name, start, expiry, permissions):
        if self.command_args['--name']:
            container_name = self.command_args['--name']
        self.result.add(
            self.account.storage_name() + ':container_sas_url',
            self.container.sas(container_name, start, expiry, permissions)
        )
        self.out.display()

    def __container_content(self, container_name):
        if self.command_args['--name']:
            container_name = self.command_args['--name']
        self.result.add(
            self.account.storage_name() + ':container_content',
            self.container.content(container_name)
        )
        self.out.display()

    def __container_list(self):
        self.result.add(
            self.account.storage_name() + ':containers',
            self.container.list()
        )
        self.out.display()

    def __container_create(self, container_name):
        if self.command_args['--name']:
            container_name = self.command_args['--name']
        log.info('Request to create container %s', container_name)
        self.container.create(container_name)
        log.info('Created %s container', container_name)

    def __container_delete(self, container_name):
        if self.command_args['--name']:
            container_name = self.command_args['--name']
        log.info('Request to delete container %s', container_name)
        self.container.delete(container_name)
        log.info('Deleted %s container', container_name)

    def __share_list(self):
        self.result.add('share_names', self.fileshare.list())
        self.out.display()

    def __share_create(self):
        share_name = self.command_args['--name']
        self.fileshare.create(share_name)
        log.info('Created Files Share %s', share_name)

    def __share_delete(self):
        share_name = self.command_args['--name']
        self.fileshare.delete(share_name)
        log.info('Deleted Files Share %s', share_name)
