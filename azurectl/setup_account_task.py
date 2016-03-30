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
       azurectl setup account configure --name=<account_name> --publish-settings-file=<file>
           [--subscription-id=<subscriptionid>]
           [--region=<region_name> --storage-account-name=<storagename> --container-name=<containername>]
       azurectl setup account list
       azurectl setup account region add --region=<region_name> --storage-account-name=<storagename> --container-name=<containername>
           [--name=<account_name>]
       azurectl setup account region default --region=<region_name>
           [--name=<account_name>]
       azurectl setup account remove --name=<account_name>
       azurectl setup account region help
       azurectl setup account help

commands:
    configure
        create new account config file
    list
        list configured account and region sections. Also list
        information about default config file
    region add
        add new region section to the config file. If specified
        the given account config file is used, otherwise the default
        config file
    region default
        set new default region in config file. If specified
        the given account config file is used, otherwise the default
        config file
    remove
        remove specified account config file
    region help
        show manual page for account region subcommand
    help
        show manual page for account command

options:
    --container-name=<containername>
        specify default container name used with the storage account
        in the selected region.
    --name=<account_name>
        account name used for account config file lookup
    --publish-settings-file=<file>
        path to the Microsoft Azure account publish settings file
    --storage-account-name=<storagename>
        specify default storage account name in the selected region.
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
from config import Config


class SetupAccountTask(CliTask):
    """
        Process setup config commands
    """
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.result = DataCollector()
        self.out = DataOutput(
            self.result,
            self.global_args['--output-format'],
            self.global_args['--output-style']
        )

        if self.command_args['list']:
            self.__list()
        else:
            self.__load_account_setup(
                self.command_args['--name']
            )
            if self.command_args['remove']:
                self.__remove()
            elif self.command_args['configure']:
                self.__configure_account()
            elif self.command_args['region'] and self.command_args['add']:
                self.__region_add()
            elif self.command_args['region'] and self.command_args['default']:
                self.__set_region_default()

    def __help(self):
        if self.command_args['region'] and self.command_args['help']:
            self.manual.show('azurectl::setup::account::region')
        elif self.command_args['help']:
            self.manual.show('azurectl::setup::account')
        else:
            return False
        return self.manual

    def __load_account_setup(self, for_account=None):
        self.setup = AccountSetup(
            Config.get_config_file(account_name=for_account)
        )

    def __configure_account(self):
        self.setup.configure_account(
            self.command_args['--name'],
            self.command_args['--publish-settings-file'],
            self.command_args['--region'],
            self.command_args['--storage-account-name'],
            self.command_args['--container-name'],
            self.command_args['--subscription-id']
        )
        self.setup.write()
        log.info(
            'Added account %s', self.command_args['--name']
        )

    def __region_add(self):
        self.setup.add_region(
            self.command_args['--region'],
            self.command_args['--storage-account-name'],
            self.command_args['--container-name']
        )
        self.setup.write()
        log.info('Added region %s', self.command_args['--region'])

    def __set_region_default(self):
        if self.setup.set_default_region(self.command_args['--region']):
            self.setup.write()
            log.info(
                'Region %s is now set as default',
                self.command_args['--region'],
            )

    def __remove(self):
        self.setup.remove()
        log.info('Removed account config file %s', self.setup.filename)

    def __list(self):
        config_files = Config.get_config_file_list()
        self.result.add(
            'default_config_file', config_files[0] or '<missing>'
        )

        for config_file in config_files:
            if config_file:
                setup = AccountSetup(config_file)
                account_info = setup.list()
                if account_info:
                    self.result.add(config_file, account_info)

        self.out.display()
