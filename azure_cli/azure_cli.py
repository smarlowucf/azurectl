#!/usr/bin/python

# core
import sys

# extensions
import docopt

# project
from app import App
from logger import Logger
from exceptions import *

def main():
    try:
        App()
    except AzureError as e:
        Logger.error('%s (%s)' %(type(e), str(e)))
        sys.exit(1)
    except docopt.DocoptExit:
        raise
        sys.exit(1)
    except SystemExit:
        raise
    except:
        Logger.error("Unexpected error:")
        raise
