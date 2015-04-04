# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ [global-options] *servicename* *command* [*args*...]

# DESCRIPTION

  Manage Microsoft Azure public cloud services from the command line in a similar fashion to other public cloud services. [Microsoft Azure](https://manage.windowsazure.com)

# SERVICE NAMES

## __compute__

Compute service which includes image and blob storage management

# COMMANDS

## __storage__

Azure blob storage and container management:

  * List storage account names
  * List storage container names
  * Show storage container contents
  * upload files to storage container
  * delete files from storage container

## __image__

Azure image management

  * List registered images

# GLOBAL OPTIONS

## __--config=file__

Location of global config file, default is: __~/.azurectl/config__

## __--account=name__

Account name to select from config file. The azurectl config file is an INI style file structured into sections. Each section takes a name and is selectable via the --account option. The default account section name if no account is selected is: __default__
