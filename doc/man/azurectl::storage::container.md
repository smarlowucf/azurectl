# NAME

azurectl - Command Line Interface to manage Microsoft Azure

Storage accounts are subdivided into containers, within which contents are
stored as binary blobs.

# SYNOPSIS

__azurectl__ storage container create

    [--name=<containername>]

__azurectl__ storage container sas

    [--name=<containername>]
    [--start-datetime=start] [--expiry-datetime=expiry]
    [--permissions=permissions]

__azurectl__ storage container list

__azurectl__ storage container show

    [--name=<containername>]

__azurectl__ storage container delete --name=<containername>

# DESCRIPTION

## __create__

Add a new container to the active storage account. If no __--name__ is
specified, the default container name from the active config file will be used.

## __delete__

Delete a container, and all of its contents, from the active storage account.

## __list__

List containers contained in the active storage account.

## __sas__

Generate a Shared Access Signature (SAS) URL allowing limited access to
a container, without requiring an access key. This SAS URL will grant access
to all blobs in the selected storage container.
See https://azure.microsoft.com/en-us/documentation/articles/storage-dotnet-shared-access-signature-part-1/
for more information on shared access signatures.

## __show__

List the names of the contents of a container.

# OPTIONS

##__--expiry-datetime=expiry__

Date (and optionally time) to cease access via a shared access signature.
(default: 30 days from start)

##__--name=containername__

Name of a container. If this option is not supplied, the default container name
from the active config file will be used.

##__--permissions=permissions__

String of permitted actions on a storage element via shared access signature.
(default: rl)

* r = Read
* w = Write
* d = Delete
* l = List

## __--start-datetime=start__

Date (and optionally time) to grant access via a shared access signature.
(default: now)

