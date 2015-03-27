import sys
from nose.tools import *
from azure_cli.cli import Cli
from azure_cli.azurectl_exceptions import *


class TestCli:
    def setup(self):
        self.command = 'help'
        self.servicename = 'compute'
        self.help_command_args = {
            '--help': False,
            '<command>': 'args',
            'compute': True,
            'help': True,
            'image': False,
            'storage': False
        }
        sys.argv = [sys.argv[0], self.servicename, self.command, 'args']
        self.cli = Cli()
        self.loaded_command = self.cli.load_command()

    def get_servicename(self):
        assert self.cli.get_servicename() == self.servicename

    def test_get_command(self):
        assert self.cli.get_command() == self.command

    def test_get_command_args(self):
        assert self.cli.get_command_args() == self.help_command_args

    def test_get_global_args(self):
        assert self.cli.get_global_args() == {
            '--config': None,
            '--account': None,
            '--version': False,
            '--help': False,
            '<servicename>': 'compute'
        }

    def test_load_command(self):
        assert self.cli.load_command() == self.loaded_command
