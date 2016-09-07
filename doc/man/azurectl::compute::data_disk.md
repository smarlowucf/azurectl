# NAME

azurectl - Command Line Interface to manage Microsoft Azure

Data-disks are virtual disks attached to a virtual machine, backed by a virtual
hard disk (VHD) image in Azure storage.

# SYNOPSIS

__azurectl__ compute data-disk create --cloud-service-name=*name* --size=*disk-size-in-GB*

    [--instance-name=name]
    [--label=label]
    [--disk-name=name]
    [--lun=lun]
    [--no-cache|--read-only-cache|--read-write-cache]
    [--wait]

__azurectl__ compute data-disk delete --disk-name=*name*

__azurectl__ compute data-disk detach --cloud-service-name=*name* --lun=*lun*

    [--instance-name=name]
    [--wait]

__azurectl__ compute data-disk list

__azurectl__ compute data-disk show --disk-name=*name*

__azurectl__ compute data-disk show attached --cloud-service-name=*name*

    [--lun=*lun*]
    [--instance-name=name]

# DESCRIPTION

## __create__

Create a new, empty data disk attached to the specified instance. The data disk vhd file will be created using the following naming schema: __(instance-name|cloud-service-name)-data-disk-(utctime)__. Example: __disk-basename-data-disk-2016-08-22T09_15_25.950289__. The default data disk size if not specified is set to 10GB.

## __delete__

Delete the specified data disk. The call will fail if the disk is still attached to an instance.

## __detach__

Detach a data disk from the selected virtual machine and retain the data disk vhd file.

## __list__

Return list of all disks from your image repository

## __show__

Return details of the specified disk

## __show attached__

Show detailed information about data disk(s), attached to the selected virtual machine. If a lun is specified only information for the disk connected to that __lun__ will be shown.

# OPTIONS

## __--cloud-service-name=name__

Name of the cloud service where the selected virtual machine may be found.

## __--disk-name=name__

Name of the disk file created in the current storage container. If omitted, a unique name will be automatically generated.

## __--instance-name=name__

Name of the virtual machine instance. If no name is given the instance name is assumed to be the same as the cloud service name.

## __--label=label__

Custom label for the data disk.

## __--lun=lun__

The logical unit number where the disk will be mounted. Must be an integer between 0 and 15. If omitted when __create__ing a disk, the first available LUN will be selected automatically.

## __--size=disk-size-in-GB__

The volume of storage capacity, in GB, that will be provisioned for this disk. Must be an integer, and less than 1024 (~ 1TB).

## CACHING OPTIONS

## __--no-cache__

Disable caching on the data disk's controller.

## __--read-only-cache__

Enable cached reads from the data disk. If a cache method is not selected, read-only will be selected by default.

## __--read-write-cache__

Enable cached reads from and writes to the data disk.

## __--wait__

wait for the request to change its status to succeeded
