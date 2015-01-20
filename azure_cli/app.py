from cli import Cli

from exceptions import *

from help_task import HelpTask
from container_task import ContainerTask
from disk_task import DiskTask
from image_task import ImageTask

class App:
    def __init__(self):
        action = Cli().get_command()
        command = None

        if action == 'help':
           command = HelpTask()
        elif action == 'container':
           command = ContainerTask()
        elif action == 'disk':
           command = DiskTask()
        elif action == 'image':
            command = ImageTask()
        else:
            raise AzureUnknownCommand(action)
        
        command.process()
