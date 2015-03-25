# extensions
from cli import Cli

# project
from exceptions import *
from cli_task import CliTask


class App:
    def __init__(self):
        app = CliTask()
        action = app.cli.get_command()
        task_class_name = action.title() + 'Task'
        task_class = app.task.__dict__[task_class_name]
        task_class().process()
