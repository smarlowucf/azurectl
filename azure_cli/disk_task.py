"""
usage: azure-cli disk upload <XZ-compressed-image> <container>
           [--max-chunk-size=<size>]
           [--name=<target_name>]
       azure-cli disk delete <name> <container>
       azure-cli disk list <container>

commands:
    upload   upload image to the given container
    delete   delete image in the given container
    list     list content of given container for configured storage account

options:
    --max-chunk-size=<size>  max chunk byte size for disk upload
    --name=<target_name>     set the target name for the container, if not set the target name is set to the basename of the image file
"""

# extensions
from apscheduler.scheduler import Scheduler

# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *
from disk import Disk
from container import Container

class DiskTask(CliTask):
    def process(self):
        container_name = self.command_args['<container>']
        self.account = AzureAccount(self.account_name, self.config_file)
        self.disk = Disk(self.account, container_name)
        self.container = Container(self.account)
        if self.command_args['upload']:
            self.__upload()
        elif self.command_args['delete']:
            self.__delete()
        elif self.command_args['list']:
            self.__list(container_name)
        else:
            raise AzureUnknownDiskCommand(self.command_args)

    def __upload(self):
        progress = Scheduler()
        progress.start()
        progress.add_interval_job(
            self.disk.print_upload_status, seconds = 2
        )
        image = self.command_args['<XZ-compressed-image>']
        self.disk.upload(
            image, self.command_args['--name'],
            self.command_args['--max-chunk-size']
        )
        progress.shutdown()
        Logger.info('Uploaded %s' % image)

    def __delete(self):
        image = self.command_args['<name>']
        self.disk.delete(image)
        Logger.info('Deleted %s' % image)

    def __list(self, container_name):
        result = DataCollector()
        result.add(
            self.account.storage_name() + ':container_content',
            self.container.content(container_name)
        )
        Logger.info(result.json(), 'Disk')
