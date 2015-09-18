# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
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
from ConfigParser import ConfigParser
import os
import sys


# project
from azurectl_exceptions import (
    AzureAccountLoadFailed,
    AzureConfigParseError,
    AzureAccountNotFound,
    AzureAccountValueNotFound
)


class Config(object):
    """
        Reading of INI style config file attributes
    """
    PLATFORM = sys.platform[:3]

    def __init__(self, account_name=None, filename=None, platform=PLATFORM):
        from logger import log

        usr_config = ConfigParser()
        self.config_files = [
            '.config/azurectl/config', '.azurectl/config'
        ]
        if not account_name:
            account_name = 'default'
        if filename and not os.path.isfile(filename):
            raise AzureAccountLoadFailed(
                'no such config file %s' % filename
            )
        elif filename:
            self.config_file = filename
        else:
            self.config_file = self.__default_config(platform)
            if not self.config_file:
                raise AzureAccountLoadFailed(
                    'could not find default configuration file %s %s: %s' %
                    (
                        ' or '.join(self.config_files),
                        'in home directory',
                        self.__home_path(platform)
                    )
                )
        try:
            log.debug('Using configuration from %s', self.config_file)
            usr_config.read(self.config_file)
        except Exception as e:
            raise AzureConfigParseError(
                'Could not parse config file: "%s"\n%s' %
                (self.config_file, e.message)
            )
        if not usr_config.has_section(account_name):
            raise AzureAccountNotFound(
                'Account %s not found' % account_name
            )
        self.config = usr_config
        self.account_name = account_name

    def get_option(self, option):
        result = ''
        try:
            result = self.config.get(self.account_name, option)
        except Exception:
            raise AzureAccountValueNotFound(
                "%s not defined for account %s" % (option, self.account_name)
            )
        return result

    def __home_path(self, platform):
        homeEnvVar = 'HOME'
        if platform == 'win':
            if 'HOMEPATH' in os.environ:
                homeEnvVar = 'HOMEPATH'
            else:
                homeEnvVar = 'UserProfile'
        return os.environ[homeEnvVar]

    def __default_config(self, platform):
        for filename in self.config_files:
            full_qualified_config = self.__home_path(platform) + '/' + filename
            if os.path.isfile(full_qualified_config):
                return full_qualified_config
        return None
