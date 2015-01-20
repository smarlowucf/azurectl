"""
usage: azure-cli help <command>
"""

from exceptions import *
from logger import Logger

class Help:
    def show(self, command):
       if not command:
           raise AzureNoCommandGiven('no help context')
       Logger.info(
           "*** help page for command %s not yet available ***" % command
       )
