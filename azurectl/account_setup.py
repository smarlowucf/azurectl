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
import ConfigParser
import os

# project
from azurectl_exceptions import *
from config import Config
from logger import log


class AccountSetup:
    """
        Implements setup methods to list, add and delete account configs
    """
    def __init__(self, filename=Config.DEFAULT_CONFIG):
        self.config = ConfigParser.ConfigParser()
        self.filename = filename
        try:
            if os.path.isfile(filename):
                log.info('Parsing config file: %s' % filename)
                self.config.read(filename)
        except Exception as e:
            raise AzureConfigParseError(
                'Could not parse config file: %s: %s' %
                (filename, format(e))
            )

    def list(self):
        accounts = {}
        for section in self.config.sections():
            accounts[section] = {}
            for option in self.config.options(section):
                accounts[section][option] = self.config.get(section, option)
        return accounts

    def remove(self, name):
        if not self.config.remove_section(name):
            log.info('Section %s does not exist' % name)
            return False
        self.__write()
        return True

    def add(self, args):
        self.__validate_publish_settings_file(
            args['publishsettings']
        )
        section_name = args['name']
        self.config.add_section(section_name)
        self.config.set(
            section_name, 'publishsettings',
            args['publishsettings']
        )
        self.config.set(
            section_name, 'storage_account_name',
            args['storage_account_name']
        )
        self.config.set(
            section_name, 'storage_container_name',
            args['storage_container_name']
        )
        self.__write()
        return True

    def __validate_publish_settings_file(self, filename):
        if not os.path.isfile(filename):
            raise AzureConfigPublishSettingsError(
                'No such Publish Settings file: %s' % filename
            )

    def __write(self):
        try:
            config_handle = open(self.filename, 'w')
            self.config.write(config_handle)
            config_handle.close()
        except Exception as e:
            raise AzureConfigWriteError(
                'Could not write config file: %s: %s' %
                (type(e).__name__, format(e))
            )
