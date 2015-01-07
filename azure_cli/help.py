"""
usage: azure-cli help <command>
"""

from exceptions import *
from logger import Logger

class Help:
    def __init__(self, args):
        self.args = args

    def show(self):
       command = self.args['<command>']
       if not command:
           raise AzureNoCommandGiven('no help context')
       Logger.info("list help for command %s" % command)
