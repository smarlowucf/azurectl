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
"""
usage: azurectl compute help -h | --help
       azurectl compute help <command>
       azurectl compute storage
           [ -h | --help]
       azurectl compute image
           [ -h | --help]

commands:
    storage  usage help for Azure blob storage operations
    image    usage help for Azure image registration operations
    help     manual page for <command>
"""

# project
from cli_task import CliTask
from help import Help


class ComputeHelpTask(CliTask):
    """
        Process help command
    """
    def process(self):
        self.help = Help()
        help_for_command = self.command_args['<command>']
        self.help.show(help_for_command)
