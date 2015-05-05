import sys
from nose.tools import *
from azure_cli.cli import Cli
from azure_cli.azurectl_exceptions import *


class TestCli:
    def setup(self):
        self.help_command_args = {
            '--container': None,
            '--expiry-datetime': '30 days from start',
            '--help': False,
            '--max-chunk-size': None,
            '--name': None,
            '--permissions': 'rl',
            '--quiet': False,
            '--source': None,
            '--start-datetime': 'now',
            '-h': False,
            'account': True,
            'compute': True,
            'container': False,
            'delete': False,
            'help': False,
            'list': True,
            'sas': False,
            'show': False,
            'storage': True,
            'upload': False
        }
        sys.argv = [
            sys.argv[0], 'compute', 'storage', 'account', 'list'
        ]
        self.cli = Cli()
        self.loaded_command = self.cli.load_command()

    def test_show_help(self):
        assert self.cli.show_help() == False

    def test_get_servicename(self):
        assert self.cli.get_servicename() == 'compute'

    def test_get_command(self):
        assert self.cli.get_command() == 'storage'

    def test_get_command_args(self):
        print self.cli.get_command_args()
        assert self.cli.get_command_args() == self.help_command_args

    def test_get_global_args(self):
        assert self.cli.get_global_args() == {
            'help': False,
            '--config': None,
            '--account': None,
            '--version': False,
            '--help': False,
            '-h': False,
            '<servicename>': 'compute'
        }

    def test_load_command(self):
        assert self.cli.load_command() == self.loaded_command
