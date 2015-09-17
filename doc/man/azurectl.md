# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ [global-options] *servicename* *command* [*args*...]

# DESCRIPTION

  Manage [Microsoft Azure](https://manage.windowsazure.com) public cloud services from the command line in a similar fashion to other public cloud services. 

# SERVICE NAMES

## __setup__

Create and Manage account setup

## __compute__

Compute service which includes image and blob storage management

# COMMANDS

Each service provides a collection of commands which are loaded as plugin when the command is requested. The following chapter lists the available commands for each service. In addition every service command provides an extra manual page with detailed information about the command capabilities using the __help__ command

## __azurectl__ __setup__ __account__ help

Configuration file setup for azurectl

  * List configured accounts
  * Add account to config file
  * Delete account from config file

## __azurectl__ __compute__ __storage__ help

Azure blob storage and container management:

  * List storage account names
  * List storage container names
  * Show storage container contents
  * Generate Shared Access Signature URLs for storage containers
  * upload files to storage container
  * delete files from storage container

## __azurectl__ __compute__ __image__ help

Azure image management

  * List registered images
  * Create OS images

# GLOBAL OPTIONS

## __--config=file__

Location of global config file, default is searched in:

1. __~/.config/azurectl/config__
2. __~/.azurectl/config__

## __--account=name__

Account name to select from config file. The azurectl config file is an INI style file structured into sections. Each section takes a name and is selectable via the --account option. The default account section name if no account is selected is: __default__

## __--output-format=format__

Print information in specified format. Supported formats are

* json

The default format is: json

## __--output-style=<style>__

Print information in specified style. Supported styles are

* color
* standard

The default style is: standard
