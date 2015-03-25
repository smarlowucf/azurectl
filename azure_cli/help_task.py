"""
usage: azure-cli help <command>
"""

# project
from cli_task import CliTask
from help import Help


class HelpTask(CliTask):
    def process(self):
        self.help = Help()
        help_for_command = self.command_args['<command>']
        self.help.show(help_for_command)
