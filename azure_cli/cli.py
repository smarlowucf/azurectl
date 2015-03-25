"""
usage:
    azure-cli -h | --help
    azure-cli -v | --version
    azure-cli [--config=<file>] [--account=<name>]
              <command> [<args>...]

commands:
    help       show detailed help page for given command
    storage    list information about storage accounts
    container  list information about containers for configured storage account
    disk       list, upload, delete disk images to/from a storage container
    image      list, register, deregister os images

global options:
    -h, --help
    -v, --version
    --config=<file>          config file, default is: ~/.azure_cli/config
    --account=<name>         account name in config file, default is: default
"""
# core
import importlib

# extensions
from docopt import docopt

# project
from exceptions import *
from version import __VERSION__


class Cli:
    """Commandline interface"""

    def __init__(self):
        self.all_args = docopt(
            __doc__,
            version='azure-cli version ' + __VERSION__,
            options_first=True
        )
        self.loaded = False
        self.command_args = self.all_args['<args>']

    def get_command(self):
        return self.all_args['<command>']

    def get_command_args(self):
        if not self.loaded:
            raise AzureCommandNotLoaded(
                '%s command not loaded' % self.get_command()
            )
        return self.__load_command_args()

    def get_global_args(self):
        result = {}
        for arg, value in self.all_args.iteritems():
            if not arg == '<command>' and not arg == '<args>':
                result[arg] = value
        return result

    def load_command(self):
        if self.loaded:
            return self.loaded
        command = self.get_command()
        if not command:
            raise AzureLoadCommandUndefined(command)
        try:
            loaded = importlib.import_module('azure_cli.' + command + '_task')
        except Exception as e:
            raise AzureUnknownCommand(command)
        self.loaded = loaded
        return self.loaded

    def __load_command_args(self):
        argv = [self.get_command()] + self.command_args
        return docopt(self.loaded.__doc__, argv=argv)
