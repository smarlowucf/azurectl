import sys
from nose.tools import *
from azure_cli.cli import Cli
from azure_cli.exceptions import *


class TestCli:
    def setup(self):
        self.command = 'help'
        self.command_args = {'<command>': 'some-command-args', 'help': True}
        sys.argv = [sys.argv[0], self.command, 'some-command-args']
        self.cli = Cli()
        self.loaded_command = self.cli.load_command()

    def test_get_command(self):
        assert self.cli.get_command() == self.command

    def test_get_command_args(self):
        assert self.cli.get_command_args() == self.command_args

    def test_get_global_args(self):
        assert self.cli.get_global_args() == {
            '--version': False,
            '--config': None,
            '--account': None,
            '--help': False
        }

    def test_load_command(self):
        assert self.cli.load_command() == self.loaded_command
