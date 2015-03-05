# Azure - azure-cli

Command Line Interface to manage
[Microsoft Azure](https://manage.windowsazure.com) services.

## Contents

  * [Motivation](#motivation)
  * [Installation](#installation)
  * [Usage](#usage)
    - [Configuration file](#configuration-file)
    - [Credentials](#credentials)
    - [Examples](#examples)
  * [Implementing commands](#implementing-commands)

## Motivation

The public cloud development team at SUSE needs command line
tools to manage, register and publish OS images to the supported
Cloud Service Providers

For the Microsoft Azure public cloud service there are management
tools available based on nodejs. On linux this toolchain spawns the
disadvantage that nodejs and its requirements cause a lot of
packaging and maintenance work

According to that we were searching for alternative solutions and
found that Microsoft provides and maintains an
[SDK for python](https://github.com/Azure/azure-sdk-for-python)
for their service. Providing the azure-cli commandline utility based
on the SDK and written in python seemed to be a more
maintainable solution.

In order to provide an easy to maintain and extensible utility the
following basic concepts applies:

* Code is covered by tests using the
  [nose](https://nose.readthedocs.org/en/latest) framework

* Commandline parsing is done as stacked solution. Each command
  defines its usage and hooks into the global program by using the
  [docopt](http://docopt.org) module. Adding new commands is made
  easy by simple interfaces and loosely coupled objects

## Installation

Installation from source can be done following the standard
python setup procedure below:

```
$ python setup.py build
$ sudo python setup.py install
```

### Usage

azure-cli uses the following basic syntax

```
azure-cli [global-options] <command> [command-options]
```

In order to call azure-cli one has to create an account configuration
file. By default azure-cli looks up the config file in

```
$ ~/.azure_cli/config
```

The config file has to specify at least the following information

* default storage account name
* path to the Publish Settings file

#### Configuration file

The structure of the config file is INI file based. It's possible to
specify information for several accounts. Each section represents one
account and is distinguished by a custom name. However if no account
name is specified at invocation time, azure-cli will lookup for a
section named: __default__

The following example outlines all possible configuration parameters
for a default account:

```
[default]
storage_account_name = some-storage
publishsettings = path-to-publish-settings-file
```

* Selecting the account is done by the __--account__ switch
* Selecting the config file is done by the __--config__ switch

#### Credentials

Access to the Azure REST interface is handled via so called Publish Settings
files. Such a file contains all keys and the subscription id for a specific
account in Azure. Before you can use azure-cli you need to make sure to have
the Publish Settings file at hand.

#### Examples

* Get short help

  ```
  $ azure-cli --help
  ```

* Get detailed help for a command

  ```
  $ azure-cli help <command>
  ```

* Get short help for a command

  ```
  $ azure-cli <command> --help
  ```

* List available storage account names

  ```
  $ azure-cli storage list
  ```

* List available containers

  ```
  $ azure-cli container list
  ```

* List, Upload or delete disk images to the blob storage

  ```
  $ azure-cli disk upload <my_image> <container>
  $ azure-cli disk delete <my_image> <container>
  $ azure-cli disk list <container>
  ```


# Implementing commands

Adding new commands to the project consists of basically four steps

1. Write up implementation classes providing the functionality you need
2. Write up a task class providing the commandline processing and output
   using the implementation classes
3. Activating the command in the App class
4. Write tests for the code

The following is a simple template to illustrate the coding process

## Write up implementation class: mycmd.py

```python
from exceptions import *

class MyCmd:
    def __init__(self, storage_account):
        self.account = storage_account

    def dig_for_gold(self):
        try:
            return "no gold found in: " + self.account.default_account
        except Exception as e:
            # make sure AzureGoldError exception exists in exceptions.py
            raise AzureGoldError('%s (%s)' %(type(e), str(e)))
```


## Write up a task class: mycmd_task.py

azure-cli autoloads all task classes it can find which results in a little
naming convention one has to follow. The name of the file must end with
__*_task__. In Addition there must be one method called __process()__ which
is called to run the processing of the command and its arguments

```python

"""
usage: azure-cli mycmd dig-for-gold

commands:
    dig-for-gold   digs for gold
"""

from cli_task import CliTask
from storage_account import StorageAccount
from data_collector import DataCollector
from logger import Logger
from exceptions import *
from mycmd import MyCmd

class MyCmdTask(CliTask):
    def process(self):
        account = StorageAccount(self.account_name, self.config_file)
        self.mycmd = MyCmd(account)
        if self.command_args['dig-for-gold']:
            result = DataCollector()
            result.add('nuggets', self.mycmd.dig_for_gold())
            Logger.info(result.get())
        else
            raise AzureUnknownCommand(self.command_args)

```

## Add new command to app.py

Edit app.py and add mycmd to the list

```python
elif action == 'mycmd':
    command = app.task.MyCmdTask()
```

## Write up test: mycmd_test.py

```python
import mock
from nose.tools import *
from azure_cli.storage_account import StorageAccount
from azure_cli.exceptions import *
from azure_cli.mycmd import MyCmd

import azure_cli

class TestMyCmd:
    def setup(self):
        account = StorageAccount('default', '../data/config')
        account.default_account = 'Kansas'
        self.mycmd = MyCmd(account)

    def test_dig_for_gold(self):
        assert self.mycmd.dig_for_gold() == "no gold found in: Kansas"
```

## Write up test: mycmd_task_test.py

```python
import sys
import mock
from nose.tools import *

import azure_cli
from azure_cli.mycmd_task import MyCmdTask

class TestMyCmdTask:
    def setup(self):
        sys.argv = [sys.argv[0], 'mycmd', 'dig-for-gold']
        self.task = MyCmdTask()
        azure_cli.mycmd_task.MyCmd = mock.Mock(
            return_value=mock.Mock()
        )

    def test_process_dig_for_gold(self):
        self.task.command_args['dig-for-gold'] = True
        self.task.process()
        self.task.mycmd.dig_for_gold.assert_called_once_with()
```

