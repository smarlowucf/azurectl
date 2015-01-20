from cli_task import CliTask
from storage_account import StorageAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *

class ContainerTask(CliTask):
    def process(self):
        account = StorageAccount(self.account_name, self.config_file)
        self.container = self.azure.Container(account)
        if self.command_args['list']:
            self.__list()
        elif self.command_args['content']:
            self.__content()
        else:
            raise AzureUnknownContainerCommand(self.command_args)

    def __list(self):
        result = DataCollector()
        result.add('containers', self.container.list())
        Logger.info(result.get())

    def __content(self):
        result = DataCollector()
        result.add('container_content', self.container.content(
            self.command_args['<name>'])
        )
        Logger.info(result.get())
