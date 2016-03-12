# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute data-disk create --cloud-service-name=*name* --size=*disk-size-in-GB*

    [--instance-name=name]
    [--label=label]
    [--disk-name=name]
    [--lun=lun]
    [--no-cache|--read-only-cache|--read-write-cache]

__azurectl__ compute data-disk show --cloud-service-name=*name* --lun=*lun*

    [--instance-name=name]

__azurectl__ compute data-disk list --cloud-service-name=*name*

    [--instance-name=name]

__azurectl__ compute data-disk delete --cloud-service-name=*name* --lun=*lun*

    [--instance-name=name]

# DESCRIPTION

## __create__

Create a new empty disk, and attach it to the selected virtual machine. If the
virtual machine's __instance-name__ is the same as the __cloud-service-name__,
the __--instance-name__ argument may be omitted.

## __show__

List information about a single data disk, attached to the selected virtual
machine at the seleted __lun__.

## __list__

List information about all data disks attached to the selected virtual machine.

Note: this is a repetitive operation that make take some time to complete.

## __delete__

Detach the data disk from the selected __lun__ of the selected virtual machine
and destroy the data file.

# OPTIONS

## __--cloud-service-name=name__

Name of the cloud service where the selected virtual machine may be found.

## __--size=disk-size-in-GB__

The volume of storage capacity, in GB, that will be provisioned for this disk.
Must be an integer, and less than 1024 (~ 1TB).

## __--instance-name=name__

Name of the virtual machine instance. If no name is given the instance name is
assumed to be the same as the cloud service name.

## __--label=label__

Custom label for the data disk.

## __--disk-name=name__

Name of the disk file created in the current storage container. If omitted, a
unique name will be automatically generated.

## __--lun=lun__

The logical unit number where the disk will be mounted. Must be an integer
between 0 and 15. If omitted when __create__ing a disk, the first available LUN
will be selected automatically.

## CACHING OPTIONS

##__--no-cache__

Disable caching on the data disk's controller.

##__--read-only-cache__

Enable cached reads from the data disk. If a cache method is not selected,
read-only will be selected by default.

##__--read-write-cache__

Enable cached reads from and writes to the data disk.
