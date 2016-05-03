# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ [global-options] *servicename* *command* [*args*...]

# DESCRIPTION

  Manage [Microsoft Azure](https://manage.windowsazure.com) public cloud
  services from the command line in a similar fashion to other public cloud
  services.

# SERVICE NAMES

## __setup__

Create and manage account configuration for __azurectl__.

## __compute__

Compute service which includes virtual machine and image management.

## __storage__

Storage service which includes storage account management and disk image
uploading.

# COMMANDS

Each service provides a collection of commands which are loaded as plugin when
the command is requested. The following chapter lists the available commands
for each service. In addition every service command provides an extra manual
page with detailed information about the command capabilities using the __help__
command.

## __azurectl__ __setup__ __account__ help

Configuration file setup for azurectl:

  * List configured accounts
  * Add account to config file
  * Delete account from config file

## __azurectl__ __setup__ __account__ region help

Configuration of Azure region settings in config files:

  * Add region settings to a config file
  * Change default region in a config file

## __azurectl__ __compute__ __data-disk__ help

Manage additional (non-root) disks available to virtual machines:

  * Create empty data-disks and make available to a virtual machine
  * List all data-disks attached to a virtual machine
  * Inspect metadata for a single data-disk
  * Delete a data-disk from a virtual machine

## __azurectl__ __compute__ __endpoint__ help

Manage forwarding of TCP & UDP traffic from public ports to virtual machines:

  * Create endpoints
  * List all endpoints connected to a virtual machine
  * Inspect metadata for a singe endpoint
  * Delete an endpoint from a virtual machine

## __azurectl__ __compute__ __image__ help

Azure image management:

  * Create OS images
  * Replicate and publish images (authorized publishing accounts only)
  * List registered OS images
  * Update OS images with additonal metadata
  * Delete OS images

## __azurectl__ __compute__ __request__ help

Manage asynchronous requests to the Azure API:

  * View the status of a request
  * Wait for a request to complete

## __azurectl__ __compute__ __reserved-ip__ help

Manage public IP address reservations:

  * Create reservations for public IPs
  * List reserved IPs
  * Inspect metadata for a single reservation
  * Release an IP by deleting its reservation

## __azurectl__ __compute__ __vm__ help

Manage virtual machines:

  * Create virtual machines from an OS image
  * List available regions and virtual machine types
  * Delete virtual machines

## __azurectl__ __storage__ __account__ help

Manage Azure storage accounts:

  * Create storage accounts
  * List all storage accounts in an Azure subscription
  * List all regions where storage accounts may be created
  * Inspect metadata for a single storage account
  * Update attributes of a storage account
  * Delete a storage account and all contents

## __azurectl__ __storage__ __container__ help

Manage containers within an Azure storage account:

  * Create containers
  * Create shared access signature (SAS) URLs for containers
  * List all containers in a storage account
  * Inspect metadata for a single container
  * Delete a storage container and all contents

## __azurectl__ __storage__ __disk__ help

Manage disk images in storage:

  * Upload a fixed-size virtual hard disk (VHD), or compressed VHD into blob
    storage as a page blob, suitable for use as an OS image
  * Delete a disk image from blob storage

## __azurectl__ __storage__ __share__ help

Manage SMB file shares in Azure storage (Azure File storage):

  * Create file shares
  * List all shares in a storage account
  * Delete a file share, including all contents

# GLOBAL OPTIONS

## __--config=file__

Location of global config file, default is searched in:

1. __~/.config/azurectl/config__
2. __~/.azurectl/config__

The azurectl config file is an INI style file structured into sections. There
are account and region sections which are handled by the
__azurectl setup account command__. The minimal structure of the config file
has the following mandatory sections:

    [DEFAULT]
    default_account = account:user
    default_region = region:region_name

    [region:region_name]
    default_storage_account = storage_account_name
    default_storage_container = storage_container_name

    [account:user]
    publishsettings = /path/to/publish_settings_file

## __--account=name__

Account name to use for operations. By default the account referenced as __default_account__ from the the DEFAULT section will be used. In the configuration file the account section is stored with a prefix named __account:<value>__. The given value must match one of the account sections.

## __--region=region__

Region name to use for operations. By default the region referenced as __default_region__ from the DEFAULT section will be used. An azure region is the name of the geographic region to run e.g virtual instances or store VHD disk images. An example region name would be __East US 2__. The value for the region has to match the region names used in Microsoft Azure. In the configuration file the region section is stored with a prefix named __region:<value>__. The given value must match one of the region sections.

## __--storage-account=name__

Storage account name to use for operations. The account name must be part of the __storage_accounts__ setup of the associated region in the configuration file

## __--storage-container=name__

Storage container name to use for operations. The container name must be part of the __storage_containers__ setup of the associated region in the configuration file

## __--output-format=format__

Print information in specified format. Supported formats are

* json

The default format is: json

## __--output-style=style__

Print information in specified style. Supported styles are

* color
* standard

The default style is: standard

## __--debug__

Enable debugging mode. In this mode azurectl is more verbose and
provides information useful to clarify processing issues.

