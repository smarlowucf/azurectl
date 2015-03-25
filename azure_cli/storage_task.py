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
usage: azurectl storage list

commands:
    list     list available storage account names
"""
# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
from storage import Storage


class StorageTask(CliTask):
    """
        Process storage command
    """
    def process(self):
        account = AzureAccount(self.account_name, self.config_file)
        self.storage = Storage(account)
        if self.command_args['list']:
            self.__list()
        else:
            raise AzureUnknownStorageCommand(self.command_args)

    def __list(self):
        result = DataCollector()
        result.add('storage_names', self.storage.list())
        Logger.info(result.json(), 'Storage')
