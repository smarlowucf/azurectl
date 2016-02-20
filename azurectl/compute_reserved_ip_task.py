# Copyright (c) 2016 SUSE.  All rights reserved.
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
usage: azurectl compute reserved_ip -h | --help
       azurectl compute reserved_ip list
       azurectl compute reserved_ip show --name=<reserved-ip-name>
       azurectl compute reserved_ip help

commands:
    list
        list IP addresses reserved within this account
    show
        list information about a single IP address reservation

options:
    --name=<reserved-ip-name>
        name of the reserved IP address
    --region=<region>
        region where the IP will be reserved
"""
# project
from logger import log
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from data_output import DataOutput
from reserved_ip import ReservedIp
from help import Help


class ComputeReservedIpTask(CliTask):
    """
        Process image commands
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

        self.account = AzureAccount(self.config)
        self.reserved_ip = ReservedIp(self.account)

        if self.command_args['list']:
            self.__list()
        if self.command_args['show']:
            self.__show()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::compute::reserved_ip')
        else:
            return False
        return self.manual

    def __list(self):
        self.result.add('reserved_ips', self.reserved_ip.list())
        self.out.display()

    def __show(self):
        self.result.add(
            'reserved_ip',
            self.reserved_ip.show(self.command_args['--name'])
        )
        self.out.display()
