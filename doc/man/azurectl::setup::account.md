# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account add --name=*account_name* --publish-settings-file=*file*

    [--subscription-id=*subscriptionid*]

__azurectl__ setup account default --name=*configname*

__azurectl__ setup account list

__azurectl__ setup account remove --name=*configname*

# DESCRIPTION

## __add__

Add an account section with the name specified in __configname__ to the config file.

## __default__

Set the default account to use if no account name is specified

## __list__

List configured account names. If no config file is specified all commands will use the default config file searched in:

1. __~/.config/azurectl/config__
2. __~/.azurectl/config__

## __remove__

Remove the configuration section specified in __configname__ from the configuration file. If the section is referenced in the DEFAULT section of the configuration file it cannot be removed without changing the default reference. This can be done with __azurectl setup account default | region default__.

# OPTIONS

## __--name=account_name__

Free form name for the azure account to use

## __--publish-settings-file=file__

The path to the Microsoft Azure publish settings file which you can download from the Microsoft management console

## __--subscription-id=subscriptionid__

If your Microsoft Azure account includes more than one subscription, your publish setttings file will contain data about all of your subscriptions. Specify a __subscriptionid__ in order to select the appropriate subscription.

If __subscriptionid__ is not supplied the first subscription listed in the publish settings file will be selected by default.
