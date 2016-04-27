# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ storage container list

__azurectl__ storage container show

    [--name=<containername>]

__azurectl__ storage container create

    [--name=<containername>]

__azurectl__ storage container delete --name=<containername>

__azurectl__ storage container sas

    [--name=<containername>]
    [--start-datetime=start] [--expiry-datetime=expiry]
    [--permissions=permissions]

# DESCRIPTION

## __list__

List container names for configured __storage_account_name__

## __show__

Show contents of configured __storage_container_name__

## __sas__

Generate a Shared Access Signature URL allowing limited access to
__storage_container_name__ without an access key. This SAS URL will grant access
to all blobs in the selected storage container.
See https://azure.microsoft.com/en-us/documentation/articles/storage-dotnet-shared-access-signature-part-1/
for more information on shared access signatures.

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
