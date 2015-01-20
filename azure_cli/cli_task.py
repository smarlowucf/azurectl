from cli import Cli
from account import Account

class CliTask:
    def __init__(self):
        cli = Cli()

        # load command module
        self.azure = cli.load_command()

        # get global and command args
        command = cli.get_command()
        self.command_args = cli.get_command_args()
        self.global_args = cli.get_global_args()
        
        # get account name and config file
        self.account_name = Account.default_account
        self.config_file = Account.default_config
        if self.global_args['--account']:
            self.account_name = self.global_args['--account']
        if self.global_args['--config']:
            self.config_file = self.global_args['--config']

