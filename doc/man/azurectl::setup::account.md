# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account list

__azurectl__ setup account remove --name=*configname*

__azurectl__ setup account add --name=*configname*

    --publish-settings-file=*file*
    --storage-account-name=*storagename*
    --container-name=*containername*

# DESCRIPTION

## __list__

List configured account names. If no config file is specified all commands will use the default config file __~/.azurectl/config__

## __remove__

Remove the account configuration stored under the specified __configname__ section from the config file

## __add__

Add an account section with the name specified in __configname__ to the config file.

# OPTIONS

## __--publish-settings-file=file__

The path to the Microsoft Azure publish settings file which you can download from the Microsoft management console

## __--storage-account-name=storagename__

The name of the storage account which holds the account specific storage containers

## __--container-name=containername__

The name of the container to use from the previously specified storage account
