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
       azurectl setup account remove --name=<configname>
       azurectl setup account add --name=<configname> --publish-settings-file=<file> --storage-account-name=<storagename> --container-name=<containername>
       azurectl setup account help

commands:
    list
        list configured account sections
    remove
        remove specified account section
    add
        add a new account section to the config file
    --name=<configname>
        section name to identify this account
    --publish-settings-file=<file>
        path to the Microsoft Azure account publish settings file
    --storage-account-name=<storagename>
        storage account name to use by default
    --container-name=<containername>
        container name for storage account to use by default
    help
        show manual page for config command
"""
# project
from cli_task import CliTask
from logger import log
from help import Help
from account_setup import AccountSetup
from data_collector import DataCollector
from data_output import DataOutput


class SetupAccountTask(CliTask):
    """
        Process setup config commands
    """
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

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::setup::account')
        else:
            return False
        return self.manual

    def __add(self):
        args = {
            'name':
                self.command_args['--name'],
            'publishsettings':
                self.command_args['--publish-settings-file'],
            'storage_account_name':
                self.command_args['--storage-account-name'],
            'storage_container_name':
                self.command_args['--container-name']
        }
        if self.setup.add(args):
            log.info('Added Account %s' % self.command_args['--name'])

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
            log.info('Removed Account %s' % self.command_args['--name'])
