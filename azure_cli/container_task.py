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
usage: azurectl container list

commands:
    list     list available containers in configured storage account
"""
# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
from container import Container


class ContainerTask(CliTask):
    def process(self):
        self.account = AzureAccount(self.account_name, self.config_file)
        self.container = Container(self.account)
        if self.command_args['list']:
            self.__list()
        else:
            raise AzureUnknownContainerCommand(self.command_args)

    def __list(self):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':containers',
            self.container.list()
        )
        Logger.info(result.json(), 'Container')
