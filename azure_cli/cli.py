"""
usage:
    azure-cli -h | --help
    azure-cli -v | --version
    azure-cli [-c | --config=<file>] [-a | --account=<name>]
              <command> [<args>...]

commands:
    help       show detailed help page for a command
    container  list, create containers

global options:
    -h, --help
    -v, --version
    -c, --config=<file>
    -a, --account=<name>
"""

import importlib
from docopt import docopt

from exceptions import *

class Cli:
    """Commandline interface"""

    def __init__(self):
        self.all_args = docopt(__doc__,
            version='azure version 0.8.1.5',
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
                if value and type(value).__name__ == 'list':
                    result[arg] = value.pop()
                else:
                    result[arg] = value
        return result

    def load_command(self):
        if self.loaded:
            return self.loaded
        command = self.get_command()
        if not command:
            raise AzureLoadCommandUndefined(command)
        try:
            loaded = importlib.import_module('azure_cli.' + command)
        except Exception as e:
            raise AzureLoadCommandError('%s (%s)' %(type(e), str(e)))
        self.loaded = loaded
        return self.loaded

    def __load_command_args(self):
        argv = [self.get_command()] + self.command_args
        return docopt(self.loaded.__doc__, argv=argv)
