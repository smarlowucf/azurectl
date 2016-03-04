# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute storage container list

__azurectl__ compute storage container show

    [--name=<containername>]

__azurectl__ compute storage container create

    [--name=<containername>]

__azurectl__ compute storage container delete --name=<containername>

__azurectl__ compute storage container sas

    [--name=<containername>]
    [--start-datetime=start] [--expiry-datetime=expiry]
    [--permissions=permissions]

# DESCRIPTION

## __list__

List container names for configured __storage_account_name__

## __show__

Show contents of configured __storage_container_name__

## __sas__

Generate a Shared Access Signature URL for __storage_container_name__

# OPTIONS

## __--start-datetime=start__

Date (and optionally time) to grant access via a shared access signature. (default: now)

##__--expiry-datetime=expiry__

Date (and optionally time) to cease access via a shared access signature. (default: 30 days from start)

##__--permissions=permissions__

String of permitted actions on a storage element via shared access signature. (default: rl)

* r = Read
* w = Write
* d = Delete
* l = List
