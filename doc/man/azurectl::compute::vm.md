# NAME

azurectl - Command Line Interface to manage Microsoft Azure

Virtual machines are created in a private IP address space, and attached to a 'cloud service' that acts as firewall, reverse proxy, and load balancer.

# SYNOPSIS

__azurectl__ compute vm create --cloud-service-name=*name* --image-name=*image*

    [--custom-data=string-or-file]
    [--instance-name=name]
    [--instance-type=type]
    [--label=label]
    [--reserved-ip-name=reserved-ip-name]
    [--password=password]
    [--ssh-private-key-file=file | --fingerprint=thumbprint]
    [--ssh-port=port]
    [--user=user]
    [--wait]

__azurectl__ compute vm reboot

    [--instance-name=name]

__azurectl__ compute vm regions

__azurectl__ compute vm show --cloud-service-name=*name*

__azurectl__ compute vm types

__azurectl__ compute vm delete --cloud-service-name=*name*

    [--instance-name=name]
    [--wait]

# DESCRIPTION

## __create__

Create a virtual machine and cloud service from a given image name. If the cloud service already exists the virtual machine is placed into the existing cloud service. If there are already running instances in the cloud service it is required to choose a unique name via the --instance-name option to avoid name conflicts which would result in an exception.

## __delete__

Delete a cloud service and all its virtual machines or only a specific virtual machine instance from the cloud service. If only a specific instance should be deleted it is required to name this instance via the --instance-name option.

## __reboot__

Reboot a cloud service virtual machine. If the cloud service holds only one instance, no instance name needs to be passed to the call. If multiple instances exists it is recommended to specify which instance should be rebooted because the default instance name matches the cloud service name.

## __regions__

List all Azure regions which are accessible via the supplied account subscription, and support virtual machines.

## __show__

Retrieves system properties for the specified cloud service and the virtual machine instances it contains and show it.

## __types__

List available instance types and their attributes

* number of core CPUs
* size of OS disk in MB
* maximum number of data disks to attach
* size of main memory in MB

# OPTIONS

## __--cloud-service-name=name__

Name of the cloud service to put the virtual machine in. If the cloud service does not exist it will be created.

## __--custom-data=string-or-file__

A string of data, or a path to a file whose contents will be injected into the new virtual machine after being base64-encoded. Waagent will store this base64-encoded data on the VM as both an attribute of __/var/lib/waagent/ovf-env.xml__ and as the sole contents of __/var/lib/waagent/CustomData__.

Note: customdata is limited to 64K; using a file larger than 64K will fail.

## __--fingerprint=thumbprint__

Thumbprint of an already existing certificate in the cloud service used for ssh public key authentication. You can find the thumbprint below the CERTIFICATES tab in the CLOUD SERVICES section on the Microsoft Azure management portal.

## __--image-name=image__

name of the VHD disk image to create the virtual machine instance from. In order to obtain a list of available images call: __azurectl compute image list__

## __--instance-name=name__

Name of the virtual machine instance. if no name is given the instance name is the same as the cloud service name.

## __--instance-type=type__

The virtual machine type in terms of storage space, memory size, etc. By default this is set to __Small__ which is the least powerful machine one can get. For more information which types are provided by Microsoft call: __azurectl compute vm types__

## __--label=label__

Custom label for the virtual machine instance.

## __--password=password__

Password for the user to login. If no password is specified SSH password based login will be disabled too.

## --reserved-ip-name=reserved-ip-name__

Name of a reserved IP address to apply as a public IP of this cloud service and the public IP of this instance.

## __--ssh-port=port__

External SSH port. Defaults to standard ssh port: 22

## __--ssh-private-key-file=file__

Path to ssh private key from which a PEM certificate will be created and uploaded to the cloud service. The fingerprint of the certificate is placed as metadata for the walinux agent which allows it to create the authorized ssh public keys and place it to the authorized_keys file for public key authentication. Each instance will be provided with such an instance
certificate.

## __--user=user__

User name for login. Defaults to: __azureuser__

## __--wait__

wait for the request to change its status to succeeded
