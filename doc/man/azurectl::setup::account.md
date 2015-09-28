# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account list

__azurectl__ setup account default --name=*configname*

__azurectl__ setup account remove --name=*configname*

__azurectl__ setup account add --name=*configname*

    --publish-settings-file=*file*
    --storage-account-name=*storagename*
    --container-name=*containername*
    [--subscription-id=*subscriptionid*]

# DESCRIPTION

## __list__

List configured account names. If no config file is specified all commands will use the default config file searched in:

1. __~/.config/azurectl/config__
2. __~/.azurectl/config__

## __default__

Set the default account to use if no account name is specified

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

## __--subscription-id=subscriptionid__

If your Microsoft Azure account includes more than one subscription, your 
publish setttings file will contain data about all of your subscriptions.
Specify a __subscriptionid__ in order to select the appropriate subscription.

If __subscriptionid__ is not supplied the first subscription listed in the 
publish settings file will be selected by default.
