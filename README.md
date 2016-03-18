# Azure - azurectl

[![Build Status](https://travis-ci.org/SUSE/azurectl.svg?branch=master)](https://travis-ci.org/SUSE/azurectl)
[![Health](https://landscape.io/github/SUSE/azurectl/master/landscape.svg?style=flat)](https://landscape.io/github/SUSE/azurectl/master)

Command Line Interface to manage
[Microsoft Azure](https://manage.windowsazure.com) services.

## Contents

  * [Motivation](#motivation)
  * [Installation](#installation)
  * [Setup](#setup)
    - [Publish Settings](#publish-settings)
    - [Configuration file](#configuration-file)
  * [Usage](#usage)
    - [Examples](#examples)
  * [Contributing](#contributing)
    - [Basics](#basics)
    - [Testing] (#testing)
    - [Implementing commands](#implementing-commands)
    - [Code Structure] (#code-structure)
  * [Compatibility] (#compatibility)
  * [Issues] (#issues)
    - [Signing GIT patches] (#signing-git-patches)

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
reuse existing dependencies reducing effort at the distribution level.
Further, Microsoft provides and maintains an
[SDK for python](https://github.com/Azure/azure-sdk-for-python)
to interact with Microsoft Azure. This results in a solution that is
easier to maintain for Linux distributors.

## Installation

Packages for azurectl are provided at the openSUSE buildservice:

```
$ zypper ar http://download.opensuse.org/repositories/Cloud:/Tools/<distribution>/ \
  azurectl
$ zypper in python-azurectl
```

Installation from source follows the standard Python setup procedure
which is wrapped into a Makefile.

```
$ make
$ sudo make install
```

## Setup

In order to call azurectl a setup procedure is required. The setup is a two
step process for each Microsoft Azure Account you want to use with azurectl

1. Download of the Publish Settings file
2. Adding an account section to the azurectl configuration file

#### Publish Settings

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

Please note, if you have multiple accounts for Azure and you're already logged
in, check that you are logged in with the account for which you would like
to download the Publish Settings file.

#### Configuration file

The azurectl command uses information stored in a configuration file. By
default the following files will be looked up in the user's home
directory (__HOMEPATH__ setting on Windows.)

1. ~/.config/azurectl/config

2. ~/.azurectl/config

An alternate location for the configuration file can be specified with the
`--config` command line option.

The configuration file uses the INI format. Each section provides information
for a given account. The default section is named __default__ and is used
when no account name is specified with the `--account` command line option.

Each configured account in the configuration file must contain the 

* default storage account name
* default storage container name
* path to the Publish Settings file

In order to create or manage the account sections in the config file,
azurectl provides the __setup__ command. The default account section
as described above could be created using the following command

```
$ azurectl setup account configure \
  --name default \
  --publish-settings-file /path/to/publish/settings/file \
  --region region
  --storage-account-name storage_account_name \
  --container-name container_name
```

### Usage

azurectl uses the following basic syntax

```
azurectl [global-options] <servicename> <command> [command-options]
```

#### Examples

* Show short help

  ```
  $ azurectl --help
  ```

* Show azurectl man page

  ```
  $ azurectl help
  ```

* Show short help for a command

  ```
  $ azurectl <servicename> <command> --help
  ```

* Show man page for a command

  ```
  $ azurectl <servicename> <command> help
  ```

* List available storage account names

  ```
  $ azurectl compute storage account list
  ```

## Contributing

azurectl is compatible with Python 2.7.x and greater

The Python project uses `pyvenv` to setup a development environment
for the desired Python version.

The following procedure describes how to create such an environment:

1. Install pyvenv

   ```
$ zypper in python-virtualenv
```

2. Create the virtual environment:

   ```
$ virtualenv-2.7 .env2
```

3. Activate the virtual environment:

   ```
$ source .env2/bin/activate
```

4. Install azurectl requirements inside the virtual environment:

   ```
$ pip2.7 install -U pip setuptools
$ pip2.7 install -r .virtualenv.dev-requirements.txt
```

5. Install azurectl in "development mode":

   ```
$ ./setup.py develop
```

Once the development environment is activated and initialized with
the project required Python modules, you are ready to work.

The __develop__ target of the `setup.py` script automatically creates
the application entry point called `azurectl`, which allows to simply
call the application from the current code base:

   ```
$ azurectl --help
```

In order to leave the development mode just call:

```
$ deactivate
```

To resume your work, change into your local Git repository and
run `source .env2/bin/activate` again. Skip step 4 and 5 as
the requirements are already installed.

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
* All patches must be signed, see [Signing GIT patches](#signing-git-patches)
  below
* All contributed code must conform to
  [flake8](https://flake8.readthedocs.org/en/latest/warnings.html)
* All code contributions must be accompanied by a test. Should you not have
  a suitable Publish Settings file to run your test you will receive help.
  However you must make a good effort in providing a test. In general we
  strive to have unit tests that are not integration tests, i.e. no
  account data is needed.
* We follow the [Semantic Versioning](http://semver.org/) scheme

1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible
   manner, and
3. PATCH version when you make backwards-compatible bug fixes.

but we do not bump the version for every change.

* Command line parsing is done as stacked solution. Each command
  defines its usage and hooks into the global program by using the
  [docopt](http://docopt.org) module. Adding new commands is made
  easy by simple interfaces and loosely coupled objects
* The file __azure_command_help.txt__ contains a dump of the Node.js
  tools help at the time we started the project. We believe there are
  some inconsistencies in the Node.js tool implementation and thus will
  deviate from this command line interface.

### Testing

Running the unit tests requires the pytest test framework. The complete
set of tests can be called as follows:

```
$ make test
```

Calling a single test works as follows:

```
$ make storage_test.py
```

Running the syntax and style check requires the flake8 framework.
Run the check as follows:

```
$ make flake8
```

Running the application from source without the need to install it
can be done as follows:

```
$ cd bin
$ ./azurectl
```

The primary focus of testing is unit testing without verification of the
integration. Therefore is is not required to have a Microsoft Azure account
to run the tests or contribute to the project. When integration tests will be
developed these will be separated from the unit tests. Once integration
testing is implemented and if you are a regular contributor to the project but
you do not have your own account we can provide access to an account that
can be used for testing. The account is sponsored by Microsoft and may not
be used to run a VM or use any services for more than 1 hour. Activity
is monitored.

### Implementing commands

Adding new commands to the project consists out of four steps

1. Write tests
2. Write the implementation classes providing the functionality you need
3. Write a task class providing the command line processing and output
   using the implementation classes (file name must end with `_task`).
4. Write a manual page


The following is a simple template to illustrate the implementation

#### Write tests

For a new command at least two tests need to be written

* mycmd_test.py
* service_mycmd_task_test.py

Tests are written using the pytest testing framework. Please refer to
the `test/unit` directory to see current implementations


#### Class implementing desired functionality: mycmd.py

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
            raise AzureGoldError(
                '%s: %s' %(type(e).__name__, format(e))
            )
```


#### Command line class: mycmd_task.py

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

from azure_account import AzureAccount
from azurectl_exceptions import *
from cli_task import CliTask
from data_collector import DataCollector
from data_output import DataOutput
from help import Help
from logger import log

from mycmd import MyCmd

class ServiceMyCmdTask(CliTask):
    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.result = DataCollector()
        self.out = DataOutput(
            self.result,
            self.global_args['--output-format'],
            self.global_args['--output-style']
        )

        self.account = AzureAccount(self.account_name, self.config_file)
        self.mycmd = MyCmd(self.account)
        if self.command_args['dig-for-gold']:
            self.result.add('nuggets', self.mycmd.dig_for_gold())
            self.out.display()
        else
            raise AzureUnknownCommand(self.command_args)

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::service::mycmd')
        else:
            return False
        return self.manual
```

#### Write manual page

Manual pages are written in github markdown and auto converted into the
man page format using the pandoc utility. Manual pages are located in:

```
$ doc/man/azurectl::service::mycmd.md
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

### Code Structure

All code needs to conform to
[flake8](https://flake8.readthedocs.org/en/latest/warnings.html).
In addition __import__ statements should be in alpha-order. The
"from ... import .." form follows at the end, also in alpha order based on
the module name from which the import occurs. Modules loaded from azurectl are
separated from the Python imported modules by the __# project__ comment.

For example:

```
import dateutil
import os

from A import B

# project
from defaults import Defaults
```

## Compatibility

As mentioned previously we believe there is room for improvement in the
Node.js based tools with respect to the command organization. Therefore
we will implement commands and functionality as we see fit with consideration
also being given to the command organization in other public cloud framework
command line tools.

A compatibility layer to match the Node.js implementation is a possibility.


## Issues

We track issues (bugs and feature requests) in the GitHub Issue tracker. As
noted above we believe that there are consistency issue in the Node.js tools
and we will not follow the command implementation of the Node.js tools 1 for
1. Therefore, please do not file issues of the form "it works like this in
Node.js tools and the command should be the same." Issues of this type will
not be accepted for the general implementation and will only apply to the
compatibility layer.

### Signing GIT Patches

With ssh keys being widely available and the increasing compute power available
to many people refactoring of SSH keys is in the range of possibilities.
Therefore SSH keys as used by GitHub as a 'login/authentication' mechanism no
longer provide the security they once did. See
[github ssh keys](http://cryptosense.com/batch-gcding-github-ssh-keys) and
[github users keys](https://blog.benjojo.co.uk/post/auditing-github-users-keys)
as reference. In an effort to ensure the integrity of the repository and the
code base patches sent for inclusion must be GPG signed. Follow the
instructions below to let git sign your commits.

1. Create a key suitable for signing (its not recommended to use
   existing keys to not mix it up with your email environment etc):

   ```
   $ gpg --gen-key
   ```

   Choose a DSA key (3) with a keysize of 2048 bits (default) and
   a validation of 3 years (3y). Enter your name/email and gpg
   will generate a DSA key for you:

   You can also choose to use an empty passphrase, despite GPG's warning,
   because you are only going to sign your public git commits with it and
   dont need it for protecting any of your secrets. That might ease later
   use if you are not using an gpg-agent that caches your passphrase between
   multiple signed git commits.

2. Add the key ID to your git config

   In above case, the ID is 11223344 so you add it to either your global
   __~/.gitconfig__ or even better to your __.git/config__ inside your
   repo:

   ```
   [user]
       name = Joe Developer
       email = developer@foo.bar
       signingkey = 11223344
   ```

   That's basically it.

3. Signing your commits

   Instead of 'git commit -a' use the following command to sign your commit

   ```
   $ git commit -S -a
   ```

4. Show signatures of the commit history

   The signatures created by this can later be verified using the following
   command:

   ```
   $ git log --show-signature
   ```
