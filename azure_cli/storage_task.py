"""
usage: azure-cli storage list

commands:
    list     list available storage account names
"""

# project
from cli_task import CliTask
from storage_account import StorageAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *
from storage import Storage

class StorageTask(CliTask):
    def process(self):
        account = StorageAccount(self.account_name, self.config_file)
        self.storage = Storage(account)
        if self.command_args['list']:
            self.__list()
        else:
            raise AzureUnknownStorageCommand(self.command_args)

    def __list(self):
        result = DataCollector()
        result.add('storage_names', self.storage.list())
        Logger.info(result.get())
