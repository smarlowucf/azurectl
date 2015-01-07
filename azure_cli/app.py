from cli import Cli
from logger import Logger

from account import Account
from storage_account import StorageAccount
from exceptions import *
from container import Container
from data_collector import DataCollector

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

        # process command
        if command == 'help':
           help = azure.Help(command_args)
           help.show()
        elif command == 'container':
           container_command = command_args['<command>']
           account = StorageAccount(account_name, config_file)
           container = Container(account)
           if container_command == 'list':
               result = DataCollector()
               result.add('containers', container.list())
               Logger.info(result.get())
           else:
               raise AzureUnknownContainerCommand(container_command)
        else:
           raise AzureUnknownCommand(command)
