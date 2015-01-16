# Azure - azure-cli

Command Line Interface to manage Azure services.

# Structure

azure-cli is a python commandline application using the following basic syntax

```
azure-cli [global-options] <command> [command-options]
```

Any of the commands are loadable modules providing the required
functionality. This allows to let the tool grow step by step
on request

# Configuration file

Access credentials to the Azure services are stored in an ini style file
like the following example:

```
[default]
storage_account_name = some-storage
publishsettings = path-to-publish-settings-file
```

The default config file is searched in $HOME/.azure\_cli/config but can
be changed by the --config switch. subscription, certificate credentials
and private keys will be imported from the publish settings file.

# Usage

get short help

```
azure-cli --help
```

get detailed help for a command

```
azure-cli help <command>
```

get short help for a command

```
azure-cli <command> --help
```

## Containers

List available containers and their contents

```
azure-cli container list
azure-cli container content <container>
```

## Disk images

Upload or delete disk images to the blob storage

```
azure-cli disk upload <my_image> <container>
azure-cli disk delete <my_image> <container>
```
# Motivation

The public cloud development team at SUSE needs command line
tools to manage, register and publish OS images to the supported
Cloud Service Providers

For the Microsoft Azure public cloud service there are management
tools available based on nodejs. On linux this toolchain spawns the
disadvantage that nodejs and its requirements cause a lot of
packaging and maintenance work

According to that we were searching for alternative solutions and
found that Microsoft provides and maintains an SDK for python for
their service. Providing a commandline utility based on the SDK
and written in python seemed to be a more maintainable solution
for us: https://github.com/Azure/azure-sdk-for-python

## Technologies used

* Code should be covered by unit tests using the nose framework
  https://nose.readthedocs.org/en/latest/

* Commandline parsing is done as stacked solution. Each command
  defines its usage and hooks into the global program by using the
  docopt module: http://docopt.org/

* Code follows python guidelines and can be used with
  python setup.py build && sudo python setup.py install



