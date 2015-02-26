# extensions
from cli import Cli

# project
from exceptions import *
from cli_task import CliTask

class App:
    def __init__(self):
        app = CliTask()
        action = app.cli.get_command()
        command = None

        if action == 'help':
           command = app.task.HelpTask()
        elif action == 'container':
           command = app.task.ContainerTask()
        elif action == 'disk':
           command = app.task.DiskTask()
        elif action == 'image':
            command = app.task.ImageTask()
        elif action == 'storage':
            command = app.task.StorageTask()
        else:
            raise AzureUnknownCommand(action)
        
        command.process()
