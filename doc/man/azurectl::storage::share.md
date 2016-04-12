# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ storage share list

__azurectl__ storage share create --name=*sharename*

__azurectl__ storage share delete --name=*sharename*

# DESCRIPTION

## __list__

List existing file share names for the configured storage account.

## __create__

The create share operation creates a new share under the specified storage account. If the share with the same name already exists, the operation fails. The name of your file share may include only lower-case characters.

## __delete__

The delete share operation marks the specified share for deletion. The share and any files contained within it are later deleted during garbage collection.
