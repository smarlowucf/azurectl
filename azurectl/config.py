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
    AzureConfigAccountNotFound,
    AzureConfigRegionNotFound,
    AzureStorageAccountInvalid,
    AzureAccountDefaultSectionNotFound,
    AzureAccountLoadFailed,
    AzureConfigVariableNotFound,
    AzureConfigSectionNotFound,
    AzureConfigParseError
)
from config_file_path import ConfigFilePath


class Config(object):
    """
        Reading of config file attributes. Any instance holds state
        information about Azure account, region, storage and container
        references
    """
    PLATFORM = sys.platform[:3]

    def __init__(
        self, account_name=None, region_name=None,
        storage_account_name=None, storage_container_name=None,
        filename=None, platform=PLATFORM
    ):
        from logger import log

        paths = ConfigFilePath(platform)

        self.account_name = account_name
        self.region_name = region_name
        self.storage_container_name = storage_container_name
        self.storage_account_name = storage_account_name

        self.config = ConfigParser()

        if filename and not os.path.isfile(filename):
            raise AzureAccountLoadFailed(
                'Could not find config file: %s' % filename
            )
        elif filename:
            self.config_file = filename
        else:
            self.config_file = paths.default_config()
            if not self.config_file:
                raise AzureAccountLoadFailed(
                    'could not find default configuration file %s %s: %s' %
                    (
                        ' or '.join(paths.config_files),
                        'in home directory',
                        paths.home_path
                    )
                )
        try:
            log.debug('Using configuration from %s', self.config_file)
            self.config.read(self.config_file)
        except Exception as e:
            raise AzureConfigParseError(
                'Could not parse config file: "%s"\n%s' %
                (self.config_file, e.message)
            )

        defaults = self.config.defaults()

        if not defaults:
            raise AzureAccountDefaultSectionNotFound(
                'could not find default section in configuration file %s' %
                self.config_file
            )

        if not self.account_name and 'default_account' in defaults:
            self.account_name = defaults['default_account']
        else:
            self.account_name = 'account:' + self.account_name
        self.__check_for_section(self.account_name)

        if not self.region_name and 'default_region' in defaults:
            self.region_name = defaults['default_region']
        else:
            self.region_name = 'region:' + self.region_name
        self.__check_for_section(self.region_name)

    def get_storage_account_name(self):
        storage_account_name = self.storage_account_name
        if not storage_account_name:
            storage_account_name = self.__get_region_option(
                'default_storage_account'
            )
        storage_accounts = self.__get_region_option('storage_accounts')
        if storage_account_name not in storage_accounts.split(','):
            raise AzureStorageAccountInvalid(
                'storage account %s not in list %s' %
                (storage_account_name, storage_accounts)
            )
        return storage_account_name

    def get_storage_container_name(self):
        storage_container_name = self.storage_container_name
        if not storage_container_name:
            storage_container_name = self.__get_region_option(
                'default_storage_container'
            )
        storage_containers = self.__get_region_option('storage_containers')
        if storage_container_name not in storage_containers.split(','):
            raise AzureStorageAccountInvalid(
                'storage container %s not in list %s' %
                (storage_container_name, storage_containers)
            )
        return storage_container_name

    def get_subscription_id(self):
        return self.__get_account_option('subscription_id')

    def get_publishsettings_file_name(self):
        return self.__get_account_option('publishsettings')

    def get_region_name(self):
        return self.region_name.replace('region:', '')

    def get_account_name(self):
        return self.account_name.replace('account:', '')

    def __check_for_section(self, section):
        if section and not self.config.has_section(section):
            raise AzureConfigSectionNotFound(
                'Section %s not found in configuration file %s' %
                (section, self.config_file)
            )

    def __get_account_option(self, option):
        if not self.account_name:
            raise AzureConfigAccountNotFound(
                'No account referenced in configuration file %s' %
                self.config_file
            )
        try:
            result = self.config.get(self.account_name, option)
        except Exception:
            raise AzureConfigVariableNotFound(
                '%s not defined for account %s in configuration file %s' %
                (option, self.account_name, self.config_file)
            )
        return result

    def __get_region_option(self, option):
        if not self.region_name:
            raise AzureConfigRegionNotFound(
                'No region referenced in configuration file %s' %
                self.config_file
            )
        try:
            result = self.config.get(self.region_name, option)
        except Exception:
            raise AzureConfigVariableNotFound(
                '%s not defined for region %s in configuration file %s' %
                (option, self.region_name, self.config_file)
            )
        return result
