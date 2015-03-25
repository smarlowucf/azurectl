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
# project
from cli import Cli
from config import Config


class CliTask:
    def __init__(self):
        self.cli = Cli()

        # load/import task module
        self.task = self.cli.load_command()

        # get command specific args
        self.command_args = self.cli.get_command_args()

        # get global args
        self.global_args = self.cli.get_global_args()

        # get account name and config file
        self.account_name = Config.DEFAULT_ACCOUNT
        self.config_file = Config.DEFAULT_CONFIG
        if self.global_args['--account']:
            self.account_name = self.global_args['--account']
        if self.global_args['--config']:
            self.config_file = self.global_args['--config']
