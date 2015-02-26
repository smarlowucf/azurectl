"""
usage: azure-cli container list
       azure-cli container content <name>

commands:
    list     list available containers
    content  list content of given container
"""

# project
from cli_task import CliTask
from storage_account import StorageAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *
from container import Container

class ContainerTask(CliTask):
    def process(self):
        self.account = StorageAccount(self.account_name, self.config_file)
        self.container = Container(self.account)
        if self.command_args['list']:
            self.__list()
        elif self.command_args['content']:
            self.__content()
        else:
            raise AzureUnknownContainerCommand(self.command_args)

    def __list(self):
        result = DataCollector()
        result.add(
            'containers:' + self.account.get_name(),
            self.container.list()
        )
        Logger.info(result.get())

    def __content(self):
        result = DataCollector()
        result.add(
            'container_content:' + self.account.get_name(),
            self.container.content(self.command_args['<name>'])
        )
        Logger.info(result.get())
