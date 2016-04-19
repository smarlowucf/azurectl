# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account configure --name=*account_name* --publish-settings-file=*file*

    [--subscription-id=subscriptionid]
    [--region=region_name --storage-account-name=storagename --container-name=containername --create]

__azurectl__ setup account configure --name=*account_name* --management-pem-file=*file* --management-url=*url* --subscription-id=*subscriptionid*

    [--region=region_name --storage-account-name=storagename --container-name=containername --create]

__azurectl__ setup account default --name=*account_name*

__azurectl__ setup account list

__azurectl__ setup account remove --name=*account_name*

# DESCRIPTION

## __configure__

Create new account configuration file

## __default__

Create a default configuration which is a symlink to the specified account configuration file. If there is already a default configuration which is not a symlink to an account configuration, the call will fail with an error message.

## __list__

List configured account names. If no config file is specified all commands will use the default config file searched in:

1. __~/.config/azurectl/config__
2. __~/.azurectl/config__

## __remove__

Remove the referenced account configuration file

# OPTIONS

## __--name=account_name__

Free form name for the azure account to use. The name is used to find the corresponding configuration file

## __--publish-settings-file=file__

The path to the Microsoft Azure publish settings file which you can download from the Microsoft management console

## __--management-pem-file=file__

If a management certificate has been created for this account, specify the absolute path of the pem file used to create the certificate.

## __--management-url=url__

If a management certificate is being used in lieu of a publish settings file, the URL of the management API needs to be specified manually as well.

Common URLs are:

* Azure: https://management.core.windows.net
* Azure China: https://management.core.chinacloudapi.cn
* Azure Black Forest: https://management.core.cloudapi.de

## __--subscription-id=subscriptionid__

If your Microsoft Azure account includes more than one subscription, your publish setttings file will contain data about all of your subscriptions. Specify a __subscriptionid__ in order to select the appropriate subscription.

If __subscriptionid__ is not supplied the first subscription listed in the publish settings file will be selected by default.

If using a management certificate, a __subscriptionid__ must be supplied.

## __--region=region__

Name of the geographic region in Azure

## __--storage-account-name=storagename__

The name of the storage account which must exist in the configured region

## __--container-name=containername__

The name of the container which must exist in the configured storage account

## __--create__

Optional paramter for the account configuration. Allows to create the storage account and its container in Azure
