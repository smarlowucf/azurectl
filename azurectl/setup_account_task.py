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
"""
usage: azurectl setup account -h | --help
       azurectl setup account configure --name=<account_name> --publish-settings-file=<file> --region=<region_name> --storage-account-name=<storagename>... --container-name=<containername>...
       azurectl setup account add --name=<account_name> --publish-settings-file=<file>
           [--subscription-id=<subscriptionid>]
       azurectl setup account default --name=<configname>
       azurectl setup account list
       azurectl setup account region add --name=<region_name> --storage-account-name=<storagename>... --container-name=<containername>...
       azurectl setup account region default --name=<configname>
       azurectl setup account remove --name=<configname>
       azurectl setup account help

commands:
    add
        add a new account section to the config file
    configure
        add a new account and region configuration to the config file
    default
        set a new default account to use if not explicitly specified
    list
        list configured account and region sections. Also list
        information about default references
    region add
        add a new region section to the config file
    region default
        set a new default region to use if not explicitly specified
    remove
        remove specified section from config file
    help
        show manual page for config command

options:
    --container-name=<containername...>
        specify container name for storage account. more container names
        can be added by providing this option multiple times. The first
        container in the list will be the default one for the specified
        region
    --name=<configname>
        section name to identify this account
    --publish-settings-file=<file>
        path to the Microsoft Azure account publish settings file
    --storage-account-name=<storagename>
        storage account name. more storage account names can be added by
        providing this option multiple times. The first storage account in
        the list will be the default one for the specified region
    --subscription-id=<subscriptionid>
        subscription id, if more than one subscription is included in your
        publish settings file.
"""
# project
from cli_task import CliTask
from logger import log
from help import Help
from account_setup import AccountSetup
from data_collector import DataCollector
from data_output import DataOutput
from azurectl_exceptions import AzureAccountLoadFailed
from config_file_path import ConfigFilePath
from config import Config


class SetupAccountTask(CliTask):
    """
        Process setup config commands
    """

    def load_config(self):
        """
            Override CliTask's load_config, gracefully handle the case
            where config file does not exist, so a new one may be added.
        """
        try:
            self.config = Config(
                self.global_args['--account'],
                self.global_args['--region'],
                self.global_args['--storage-account'],
                self.global_args['--storage-container'],
                self.global_args['--config']
            )
            self.config_file = self.config.config_file
        except AzureAccountLoadFailed:
            if self.command_args['configure']:
                self.config_file = ConfigFilePath().default_new_config()
            else:
                raise

    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.setup = AccountSetup(self.config_file)

        self.result = DataCollector()
        self.out = DataOutput(
            self.result,
            self.global_args['--output-format'],
            self.global_args['--output-style']
        )

        if self.command_args['list']:
            self.__list()
        elif self.command_args['remove']:
            self.__remove()
        elif self.command_args['configure']:
            self.__configure_account_and_region()
        elif self.command_args['add'] and self.command_args['region']:
            self.__region_add()
        elif self.command_args['add']:
            self.__account_add()
        elif self.command_args['default'] and self.command_args['region']:
            self.__set_region_default()
        elif self.command_args['default']:
            self.__set_account_default()

        if not self.command_args['list']:
            self.setup.write()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::setup::account')
        else:
            return False
        return self.manual

    def __configure_account_and_region(self):
        self.setup.configure_account_and_region(
            self.command_args['--name'],
            self.command_args['--publish-settings-file'],
            self.command_args['--region'],
            self.command_args['--storage-account-name'][0],
            self.command_args['--container-name'][0],
            self.command_args['--storage-account-name'],
            self.command_args['--container-name'],
            self.command_args['--subscription-id']
        )
        log.info(
            'Added account %s with region %s',
            self.command_args['--name'],
            self.command_args['--region']
        )

    def __account_add(self):
        self.setup.add_account(
            self.command_args['--name'],
            self.command_args['--publish-settings-file'],
            self.command_args['--subscription-id']
        )
        log.info('Added account %s', self.command_args['--name'])

    def __region_add(self):
        self.setup.add_region(
            self.command_args['--name'],
            self.command_args['--storage-account-name'][0],
            self.command_args['--container-name'][0],
            self.command_args['--storage-account-name'],
            self.command_args['--container-name']
        )
        log.info('Added region %s', self.command_args['--name'])

    def __set_account_default(self):
        if self.setup.set_default_account(
            self.command_args['--name']
        ):
            log.info(
                'Account %s is now set as default account',
                self.command_args['--name']
            )

    def __set_region_default(self):
        if self.setup.set_default_region(
            self.command_args['--name']
        ):
            log.info(
                'Region %s is now set as default account',
                self.command_args['--name']
            )

    def __list(self):
        account_info = self.setup.list()
        if not account_info:
            log.info('There are no accounts configured')
        else:
            self.result.add('setup', account_info)
            self.out.display()

    def __remove(self):
        if self.setup.remove(
            self.command_args['--name']
        ):
            log.info('Removed config section %s', self.command_args['--name'])
