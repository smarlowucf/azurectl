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
       azurectl compute image help

commands:
    list
        list available os images for configured account
    help
        show manual page for image command
"""
# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
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

        account = AzureAccount(self.account_name, self.config_file)
        self.image = Image(account)
        if self.command_args['list']:
            self.__list()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::compute::image')
        else:
            return False
        return self.manual

    def __list(self):
        result = DataCollector()
        result.add('images', self.image.list())
        Logger.info(result.json(), 'Image')
