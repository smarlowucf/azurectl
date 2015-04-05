# Azure - azurectl

Command Line Interface to manage
[Microsoft Azure](https://manage.windowsazure.com) services.

## Contents

  * [Motivation](#motivation)
  * [Installation](#installation)
  * [Usage](#usage)
    - [Configuration file](#configuration-file)
    - [Credentials](#credentials)
    - [Examples](#examples)
  * [Contributing](#contributing)
    - [Dependencies](#dependencies)
    - [Basics](#basics)
    - [Setup](#setup)
    - [Implementing commands](#implementing-commands)

## Motivation

Manage Microsoft Azure public cloud services from the command line in
a similar fashion to other public cloud services.

Command line tools for Microsoft Azure already exist. The existing
tool is based on Node.js and is available on GitHub. The dependency
management model associated with the Node.js package management tool,
npm, generates a considerably higher package and package maintenance
work load for Linux distributions than tools based on other languages.
For community distributions this implies an increased effort by
volunteers and for Enterprise distributions it may lead to a stack that
cannot be supported. Therefore, a tool implemented in another language
provides a significant improvement for Linux distributions.

For this project we chose Python as the implementation language. Other
public cloud command line tools are also based on Python and thus we can
reuse existing dependencies for other tools reducing effort at the
distribution level. Further, Microsoft provides and maintains an
[SDK for python](https://github.com/Azure/azure-sdk-for-python)
to interact with Microsoft Azure. This results in a solution that is
easier to maintain for Linux distributors.

## Installation

Installation from source follows the standard Python setup procedure.

```
$ python setup.py build
$ sudo python setup.py install
```

### Usage

azurectl uses the following basic syntax

```
azurectl [global-options] <servicename> <command> [command-options]
```

In order to call azurectl one has to create an account configuration
file. By default azurectl looks up the config file in

#### Configuration file

The azurectl command uses information stored in a configuration file. By
default the file is located in a directory named __.azurectl__ in the
user's home directory (__HOMEPATH__ setting on Windows.)

```
$ ~/.azurectl/config
```

An alternate location for the configuration file can be specified with the
`--config` command line option.

The configuration file uses the INI format. Each section provides information
for a given account. The default section is named __default__ and is used
when no account name is specified with the `--account` command line option.

Each configured account in the configuration file must contain the 

* default storage account name
* path to the Publish Settings file

The following example outlines all possible configuration parameters
for a default account:

```
[default]
storage_account_name = some-storage
storage_container_name = container-name
publishsettings = path-to-publish-settings-file
```

#### Credentials

Access to the Azure REST interface requires credentials associated with
a specific account. These credentials are provided by Azure in the
Publish Settings file. The file contains all keys and the subscription id
for a given account in Azure. The azurectl command will extract the required
information from the Publish Settings file specified in the configuration
file.

To download the Publish Settings file for your account visit
https://manage.windowsazure.com/publishsettings . If you are already
logged in, the Publish Settings file for the corresponding account
will be offered as download, otherwise you will be redirected to
the login page and need to login with your Azure account.

Please note if you have multiple accounts for Azure and you're already logged
in, check that you are logged in with the account for which you would like
to download the Publish Settings file.

#### Examples

* Get short help

  ```
  $ azurectl --help
  ```

* Get manual page for azurectl

  ```
  $ azurectl help
  ```

* Get short help for a command

  ```
  $ azurectl <servicename> <command> --help
  ```

* Get manual page for a command

  ```
  $ azurectl <servicename> <command> help
  ```

* List available storage account names

  ```
  $ azurectl compute storage account list
  ```

* List available containers

  ```
  $ azurectl compute storage container list
  ```

* List disk images of the blob storage

  ```
  $ azurectl compute image list
  ```

* Upload disk images to the blob storage

  ```
  $ azurectl compute storage upload --source <xz-image> --name <name>
  ```

* Delete disk images from the blob storage

  ```
  $ azurectl compute storage delete --name <name>
  ```

## Contributing

### Dependencies

azurectl is compatible with Python 2.7.x and greater

#### Runtime

* APScheduler > version 3.0
* azure-sdk
* docopt
* futures (for Python 2)
* pyliblzma
* man

#### Testing

* mock 
* nose
* pandoc 

### Basics

* After cloning the repo from GitHub set up a link to the project provided
  commit hook

```
$ pushd .git
$ rm -rf hooks
$ ln -s ../.git-hooks hooks
$ popd
```
We maintain a hook script to do some rudimentary local checking to catch
obvious issues that would prevent a pull request from being accepted.
* All contributed code must conform to [PEP8](https://www.python.org/dev/peps/pep-0008/)
* All code contributions must be accompanied by a test. Should you not have
  a suitable Publish Settings file to run your test you will receive help.
  However you must make a good effort in providing a test.
* We follow the [Semantic Versioning](http://semver.org/) scheme

1.) MAJOR version when you make incompatible API changes,
2.) MINOR version when you add functionality in a backwards-compatible manner, and
3.) PATCH version when you make backwards-compatible bug fixes.

but we do not bump the version for every change.
* Command line parsing is done as stacked solution. Each command
  defines its usage and hooks into the global program by using the
  [docopt](http://docopt.org) module. Adding new commands is made
  easy by simple interfaces and loosely coupled objects
* The file __azure_command_help.txt__ contains a dump of the Node.js
  tools help at the time we started the project. We believe there are
  some inconsitencies in the Node.js tool implementation and thus will
  deviate from this command line interface.

### Testing

Running the unit tests requires access to a Microsoft Azure account. If
you are a regular contributor to the project and you do not have your own
account we can provide access to an account that can be used for testing. The
account is sponsored by Microsoft and may not be used to run a VM or use any
services for more than 1 hour. Acitvity is monitored.

You need to setup you ~/.azurectl/config with a [default] section. The
storage_account_name is available in the web console and determines in
which region you are working in.

### Implementing commands

Adding new commands to the project consists of four steps

1. Write the implementation classes providing the functionality you need
2. Write a task class providing the command line processing and output
   using the implementation classes (file name must end with `_task`).
3. Write a manual page
4. Write tests

The following is a simple template to illustrate the implementation

### Class implementing desired functionality: mycmd.py

```python
from azurectl_exceptions import *

class MyCmd:
    def __init__(self, account):
        self.account = account

    def dig_for_gold(self):
        try:
            return "no gold found in: " + self.account.default_account
        except Exception as e:
            # make sure AzureGoldError exception exists in exceptions.py
            raise AzureGoldError('%s (%s)' %(type(e), str(e)))
```


### Command line class: mycmd_task.py

azurectl autoloads all task classes it can find. The established naming
convention is that the file ends with `_task.py`. The class must implement
the `process()` method. This method is called to process the command
and its arguments.

```python

"""
usage: azurectl service mycmd -h | --help
       azurectl service mycmd dig-for-gold
       azurectl service mycmd help

commands:
    dig-for-gold
        digs for gold
    help
        show manual page
"""

from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from logger import Logger
from azurectl_exceptions import *
from help import Help

from mycmd import MyCmd

class ServiceMyCmdTask(CliTask):
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.account = AzureAccount(self.account_name, self.config_file)
        self.mycmd = MyCmd(self.account)
        if self.command_args['dig-for-gold']:
            result = DataCollector()
            result.add('nuggets', self.mycmd.dig_for_gold())
            Logger.info(result.json(), 'GoldDigger')
        else
            raise AzureUnknownCommand(self.command_args)

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::service::mycmd')
        else:
            return False
        return self.manual
```

### Write manual page

Manual pages are written in github markdown and auto converted into the
man format using the pandoc utility. The manual page for _mycmd_ needs to
be created here:

```
$ vi doc/man/azurectl::service::mycmd.md
```

and should follow the basic manual page structure:

```
# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ service mycmd dig-for-gold

# DESCRIPTION

Digs for gold
```

### Write tests: mycmd_test.py, service_mycmd_task_test.py

Tests are written using the nose testing framework. Please refer to
the `test/unit` directory to see current implementations
