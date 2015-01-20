from cli_task import CliTask

class HelpTask(CliTask):
    def process(self):
        help = self.azure.Help()
        help_for_command = self.command_args['<command>']
        help.show(help_for_command)
