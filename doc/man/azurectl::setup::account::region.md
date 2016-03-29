# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ setup account region add --region=*region_name* --storage-account-name=*storagename* --container-name=*containername*
    [--name=*account_name*]

__azurectl__ setup account region default --region=*region_name*
    [--name=*account_name*]

# DESCRIPTION

## __add__

Add a new region with name: __region_name__ to the config file. The
region name must be an existing geographic region in Azure

## __default__

Set the default region to use if no region name is specified

# OPTIONS

## __--name=region_name__

Name of the geographic region in Azure

## __--storage-account-name=storagename__

The name of the storage account which must exist in the configured region

## __--container-name=containername__

The name of the container which must exist in the configured storage account

## __--name=account_name__

Free form name for the azure account to use. The name is used to find the corresponding configuration file for the region setup
