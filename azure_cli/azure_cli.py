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
        # known exception, log information and exit
        Logger.error('%s (%s)' % (type(e), str(e)))
        sys.exit(1)
    except docopt.DocoptExit:
        # exception caught by docopt, results in usage message
        raise
    except SystemExit:
        # user exception, program aborted by user
        sys.exit(1)
    except:
        # exception we did no expect, show python backtrace
        Logger.error("Unexpected error:")
        raise
