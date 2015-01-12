from cli import Cli
from logger import Logger

from account import Account
from storage_account import StorageAccount
from exceptions import *
from container import Container
from disk import Disk
from data_collector import DataCollector
from apscheduler.scheduler import Scheduler

class App:
    def __init__(self):
        cli = Cli()

        # load command module
        azure = cli.load_command()

        # get global and command args
        command = cli.get_command()
        command_args = cli.get_command_args()
        global_args = cli.get_global_args()

        # get account name and config file
        account_name = Account.default_account
        config_file = Account.default_config
        if global_args['--account']:
            account_name = global_args['--account']
        if global_args['--config']:
            config_file = global_args['--config']

        # help
        if command == 'help':
           help = azure.Help(command_args)
           help.show()

        # container
        elif command == 'container':
           account = StorageAccount(account_name, config_file)
           container = Container(account)
           if command_args['list']:
               result = DataCollector()
               result.add('containers', container.list())
               Logger.info(result.get())
           elif command_args['content']:
               result = DataCollector()
               result.add('container_content', container.content(
                   command_args['<name>'])
               )
               Logger.info(result.get())
           else:
               raise AzureUnknownContainerCommand(command_args)

        # disk
        elif command == 'disk':
           account = StorageAccount(account_name, config_file)
           disk = Disk(account, command_args['<container>'])
           if command_args['upload']:
               progress = Scheduler()
               progress.start()
               progress.add_interval_job(
                   disk.print_upload_status, seconds = 2
               )
               image = command_args['<image>']
               disk.upload(
                   image,
                   global_args['--max-data-size'],
                   global_args['--max-chunk-size']
               )
               progress.shutdown()
               Logger.info('Uploaded %s' % image)
           elif command_args['delete']:
               image = command_args['<image>']
               disk.delete(image)
               Logger.info('Deleted %s' % image)
           else:
               raise AzureUnknownDiskCommand(command_args)

        # unknown
        else:
           raise AzureUnknownCommand(command)
