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
usage: azurectl compute image -h | --help
       azurectl compute image list
       azurectl compute image create --name=<imagename> --blob=<blobname>
           [--container=<container>]
           [--label=<imagelabel>]
       azurectl compute image delete --name=<imagename>
           [--delete-disk]
       azurectl compute image help

commands:
    list
        list available os images for configured account
    create
        create OS image from VHD disk stored on blob storage container
    --container=<container>
        container name, overwrites configuration value
    --delete-disk
        on deletion of the image also delete the associated VHD disk
    --label=<imagelabel>
        image label on create, defaults to name if not set
    --name=<imagename>
        image name on create
    --blob=<blobname>
        filename of disk image as it is stored on the blob storage
    help
        show manual page for image command
"""
# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from data_output import DataOutput
from logger import log
from image import Image
from help import Help


class ComputeImageTask(CliTask):
    """
        Process image commands
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

        account = AzureAccount(self.account_name, self.config_file)
        self.image = Image(account)
        if self.command_args['list']:
            self.__list()
        elif self.command_args['create']:
            self.__create()
        elif self.command_args['delete']:
            self.__delete()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::compute::image')
        else:
            return False
        return self.manual

    def __create(self):
        self.result.add(
            'image:' + self.command_args['--name'],
            self.image.create(
                self.command_args['--name'],
                self.command_args['--blob'],
                self.command_args['--label'],
                self.command_args['--container']
            )
        )
        self.out.display()

    def __delete(self):
        self.result.add(
            'image:' + self.command_args['--name'],
            self.image.delete(
                self.command_args['--name'],
                self.command_args['--delete-disk'],
            )
        )
        self.out.display()

    def __list(self):
        self.result.add('images', self.image.list())
        self.out.display()
