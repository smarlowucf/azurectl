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
       azurectl setup account list
       azurectl setup account default --name=<configname>
       azurectl setup account remove --name=<configname>
       azurectl setup account add --name=<configname> --publish-settings-file=<file> --storage-account-name=<storagename> --container-name=<containername>
           [--subscription-id=<subscriptionid>]
       azurectl setup account help

commands:
    list
        list configured account sections
    remove
        remove specified account section
    add
        add a new account section to the config file
    default
        set a new default account to use if not explicitly specified
    help
        show manual page for config command

options:
    --name=<configname>
        section name to identify this account
    --publish-settings-file=<file>
        path to the Microsoft Azure account publish settings file
    --storage-account-name=<storagename>
        storage account name to use by default
    --container-name=<containername>
        container name for storage account to use by default
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
                self.global_args['--config']
            )
            self.config_file = self.config.config_file
        except AzureAccountLoadFailed:
            if self.command_args['add']:
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
        elif self.command_args['add']:
            self.__add()
        elif self.command_args['default']:
            self.__set_default()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::setup::account')
        else:
            return False
        return self.manual

    def __add(self):
        if self.setup.add(
            self.command_args['--name'],
            self.command_args['--publish-settings-file'],
            self.command_args['--storage-account-name'],
            self.command_args['--container-name'],
            self.command_args['--subscription-id']
        ):
            log.info('Added Account %s', self.command_args['--name'])

    def __set_default(self):
        if self.setup.set_default_account(
            self.command_args['--name']
        ):
            log.info(
                'Account %s is now set as default account',
                self.command_args['--name']
            )

    def __list(self):
        account_info = self.setup.list()
        if not account_info:
            log.info('There are no accounts configured')
        else:
            self.result.add('accounts', account_info)
            self.out.display()

    def __remove(self):
        if self.setup.remove(
            self.command_args['--name']
        ):
            log.info('Removed Account %s', self.command_args['--name'])
