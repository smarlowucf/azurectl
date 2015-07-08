# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute vm create --cloud-service-name=*name* --region=*location* --image-name=*image*

    [--custom-data=base64_string]
    [--instance-name=name]
    [--instance-type=type]
    [--label=label]
    [--password=password]
    [--ssh-private-key-file=file | --fingerprint=thumbprint]
    [--ssh-port=port]
    [--user=user]

__azurectl__ compute vm delete --cloud-service-name=*name*

    [--instance-name=name]

__azurectl__ compute vm types

# DESCRIPTION

## __create__

Create a virtual machine and cloud service from a given image name. If the cloud service already exists the virtual machine is placed into the existing cloud service. If there are already running instances in the cloud service it is required to choose a unique name via the --instance-name option to avoid name conflicts which would result in an exception.

## __delete__

Delete a cloud service and all its virtual machines or only a specific virtual machine instance from the cloud service. If only a specific instance should be deleted it is required to name this instance via the --instance-name option.

## __types__

List available instance types and their attributes

* number of core CPUs
* size of OS disk in MB
* maximum number of data disks to attach
* size of main memory in MB

# OPTIONS

## __--cloud-service-name=name__

Name of the cloud service to put the virtual machine in. If the cloud service does not exist it will be created.

## __--region=location__

Geographic region to run the virtual image in. Please note the region the VHD disk is stored may not be different from the region the instance should run. If this is a different location the service will respond with an exception.

## __--image-name=image__

name of the VHD disk image to create the virtual machine instance from. In order to obtain a list of available images call: __azurectl compute image list__

## __--custom-data=base64_string__

A base64 encoded raw stream. The information is available from the walinux agent in the running virtual machine.

## __--instance-name=name__

Name of the virtual machine instance. if no name is given the instance name is the same as the cloud service name.

## __--instance-type=type__

The virtual machine type in terms of storage space, memory size, etc. By default this is set to __Small__ which is the least powerful machine one can get. For more information which types are provided by Microsoft call: __azurectl compute vm types__

## __--label=label__

Custom label for the virtual machine instance.

## __--password=password__

Password for the user to login. If no password is specified SSH password based login will be disabled too.

## __--ssh-private-key-file=file__

Path to ssh private key from which a PEM certificate will be created and uploaded to the cloud service. The fingerprint of the certificate is placed as metadata for the walinux agent which allows it to create the authorized ssh public keys and place it to the authorized_keys file for public key authentication. Each instance will be provided with such an instance certificate.

## __--fingerprint=thumbprint__

Thumbprint of an already existing certificate in the cloud service used for ssh public key authentication. You can find the thumbprint below the CERTIFICATES tab in the CLOUD SERVICES section on the Microsoft Azure management console.

## __--ssh-port=port__

External SSH port. Defaults to standard ssh port: 22

## __--user=user__

User name for login. Defaults to: __azureuser__
