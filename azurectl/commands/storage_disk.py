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
usage: azurectl storage disk -h | --help
       azurectl storage disk upload --source=<file>
           [--blob-name=<blobname>]
           [--max-chunk-size=<size>]
           [--quiet]
       azurectl storage disk delete --name=<blobname>
       azurectl storage disk help

commands:
    delete
        delete disk image from the given container
    help
        show manual page for disk command
    upload
        upload xz compressed disk image to the given container

options:
    --blob-name=<blobname>
        name of the file in the storage pool
    --max-chunk-size=<size>
        max chunk size in bytes for upload, default 4MB
    --quiet
        suppress progress information on upload
    --source=<file>
        file to upload
"""
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

# project
from base import CliTask
from ..account.service import AzureAccount
from ..storage.storage import Storage
from ..logger import log
from ..help import Help


class StorageDiskTask(CliTask):
    """
        Process disk commands
    """
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.load_config()

        self.account = AzureAccount(self.config)

        container_name = self.account.storage_container()

        self.storage = Storage(
            self.account, container_name
        )

        if self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::storage::disk')
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
            self.command_args['--blob-name'],
            self.command_args['--max-chunk-size']
        )

    def __delete(self):
        image = self.command_args['--blob-name']
        self.storage.delete(image)
        log.info('Deleted %s', image)
