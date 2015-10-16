# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account configure --name=*account_name* --publish-settings-file=*file* --region=*region_name* --storage-account-name=*storagename* --container-name=*containername*

# DESCRIPTION

## __configure__

Add an account section with its corresponding region based storage account information

# OPTIONS

## __--name=account_name__

Free form name for the azure account to use

## __--publish-settings-file=file__

The path to the Microsoft Azure publish settings file which you can download from the Microsoft management console

## __--region=region__

Name of the geographic region in Azure

## __--storage-account-name=storagename__

The name of the storage account which must exist in the configured region

## __--container-name=containername__

The name of the container which must exist in the configured storage account
