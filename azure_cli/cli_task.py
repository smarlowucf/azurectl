# project
from cli import Cli
from config import Config

class CliTask:
    def __init__(self):
        self.cli = Cli()

        # load/import task module
        self.task = self.cli.load_command()

        # get command specific args
        self.command_args = self.cli.get_command_args()

        # get global args
        self.global_args = self.cli.get_global_args()
        
        # get account name and config file
        self.account_name = Config.default_account
        self.config_file = Config.default_config
        if self.global_args['--account']:
            self.account_name = self.global_args['--account']
        if self.global_args['--config']:
            self.config_file = self.global_args['--config']

