import ConfigParser
import os

from exceptions import *

class Account:
    default_config  = os.environ['HOME'] + '/.azure_cli/config'
    default_account = 'default'

    def __init__(self, account=default_account, filename=default_config):
        config = ConfigParser.ConfigParser()
        if not os.path.isfile(filename):
            raise AzureAccountLoadFailed('no such config file %s' % filename)
        config.read(filename)
        if not config.has_section(account):
            raise AzureAccountNotFound("Account %s not found" % account)
        self.config  = config
        self.account = account

    def read(self, option):
        result = ''
        try:
            result = self.config.get(self.account, option)
        except:
            raise AzureAccountValueNotFound(
                "%s not defined for account %s" %(option, self.account)
            )
        return result
