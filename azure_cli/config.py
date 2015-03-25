# core
import os

# extensions
import ConfigParser

# project
from exceptions import *


class Config:
    DEFAULT_CONFIG = os.environ['HOME'] + '/.azure_cli/config'
    DEFAULT_ACCOUNT = 'default'

    def __init__(self, account_name=DEFAULT_ACCOUNT, filename=DEFAULT_CONFIG):
        config = ConfigParser.ConfigParser()
        if not os.path.isfile(filename):
            raise AzureAccountLoadFailed('no such config file %s' % filename)
        config.read(filename)
        if not config.has_section(account_name):
            raise AzureAccountNotFound("Account %s not found" % account_name)
        self.config = config
        self.account_name = account_name
        self.config_file = filename

    def read(self, option):
        result = ''
        try:
            result = self.config.get(self.account_name, option)
        except:
            raise AzureAccountValueNotFound(
                "%s not defined for account %s" % (option, self.account_name)
            )
        return result
