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
from cli import Cli

# project
from azurectl_exceptions import *
from cli_task import CliTask


class App:
    """
        Application class to create task instances and process them
    """
    def __init__(self):
        app = CliTask()
        action = app.cli.get_command()
        service = app.cli.get_servicename()
        task_class_name = service.title() + action.title() + 'Task'
        task_class = app.task.__dict__[task_class_name]
        task_class().process()