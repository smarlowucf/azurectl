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
from azurectl_exceptions import (
    AzureConfigParseError,
    AzureConfigAddAccountSectionError,
    AzureConfigPublishSettingsError,
    AzureConfigWriteError
)
from logger import log


class AccountSetup(object):
    """
        Implements setup methods to list, add and delete account configs
    """
    def __init__(self, filename):
        self.config = ConfigParser.ConfigParser()
        self.filename = filename
        try:
            if os.path.isfile(filename):
                self.config.read(filename)
        except Exception as e:
            raise AzureConfigParseError(
                'Could not parse config file: %s: %s' %
                (filename, format(e))
            )

    def list(self):
        """
            list account sections
        """
        accounts = {}
        for section in self.config.sections():
            accounts[section] = {}
            for option in self.config.options(section):
                accounts[section][option] = self.config.get(section, option)
        return accounts

    def remove(self, name):
        """
            remove specified account section
        """
        if not self.config.remove_section(name):
            log.info('Section %s does not exist', name)
            return False
        self.__write()
        return True

    def add(
        self,
        section_name,
        publish_settings,
        storage_account,
        storage_container,
        subscription_id=None
    ):
        """
            add new account section
        """
        self.__validate_publish_settings_file(
            publish_settings
        )
        try:
            self.config.add_section(section_name)
        except Exception as e:
            raise AzureConfigAddAccountSectionError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        self.config.set(
            section_name, 'publishsettings', publish_settings
        )
        self.config.set(
            section_name, 'storage_account_name', storage_account
        )
        self.config.set(
            section_name, 'storage_container_name', storage_container
        )
        if subscription_id:
            self.config.set(
                section_name, 'subscription_id', subscription_id
            )
        self.__write()
        return True

    def __validate_publish_settings_file(self, filename):
        """
            validate given publish settings file for
            + existence
        """
        if not os.path.isfile(filename):
            raise AzureConfigPublishSettingsError(
                'No such Publish Settings file: %s' % filename
            )

    def __write(self):
        """
            write out config data to file
        """
        try:
            config_dir = os.path.dirname(self.filename)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            config_handle = open(self.filename, 'w')
            self.config.write(config_handle)
            config_handle.close()
        except Exception as e:
            raise AzureConfigWriteError(
                'Could not write config file: %s: %s' %
                (type(e).__name__, format(e))
            )
