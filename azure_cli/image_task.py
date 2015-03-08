"""
usage: azure-cli image list

commands:
    list     list available os images for account subscription
"""

# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *
from image import Image

class ImageTask(CliTask):
    def process(self):
        account = AzureAccount(self.account_name, self.config_file)
        self.image = Image(account)
        if self.command_args['list']:
            self.__list()

    def __list(self):
        result = DataCollector()
        result.add('images', self.image.list())
        Logger.info(result.json(), 'Image')
