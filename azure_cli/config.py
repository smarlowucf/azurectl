# Copyright (c) SUSE Linux GmbH.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import ConfigParser

# project
from azurectl_exceptions import *


class Config:
    """
        Reading of INI style config file attributes
    """
    DEFAULT_CONFIG = os.environ['HOME'] + '/.azurectl/config'
    DEFAULT_ACCOUNT = 'default'

    def __init__(self, account_name=DEFAULT_ACCOUNT, filename=DEFAULT_CONFIG):
        usr_config = ConfigParser.ConfigParser()
        if not os.path.isfile(filename):
            raise AzureAccountLoadFailed('no such config file %s' % filename)
        usr_config.read(filename)
        if not usr_config.has_section(account_name):
            raise AzureAccountNotFound("Account %s not found" % account_name)
        self.config = usr_config
        self.account_name = account_name
        self.config_file = filename

    def get_option(self, option):
        result = ''
        try:
            result = self.config.get(self.account_name, option)
        except:
            raise AzureAccountValueNotFound(
                "%s not defined for account %s" % (option, self.account_name)
            )
        return result
