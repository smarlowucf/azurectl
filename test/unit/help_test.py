import sys
from nose.tools import *
from azure_cli.help import Help
from azure_cli.azurectl_exceptions import *


class TestHelp:
    def setup(self):
        self.help = Help()

    @raises(AzureNoCommandGiven)
    def test_show(self):
        self.help.show(None)
