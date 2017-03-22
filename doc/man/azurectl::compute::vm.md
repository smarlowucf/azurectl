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

__azurectl__ compute vm shutdown --cloud-service-name=*name*
    [--instance-name=name]
    [--deallocate-resources]
    [--wait]

__azurectl__ compute vm start --cloud-service-name=*name*
    [--instance-name=name]
    [--wait]

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

## __shutdown__

Shuts down a cloud service virtual machine. The same rules with regards to the reboot of an instance applies in terms of specifying which machine should be shut down.

## __start__

Starts a cloud service virtual machine. The same rules with regards to the reboot of an instance applies in terms of specifying which machine should be started.

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

A string of data, or a path to a file whose contents will be injected into the new virtual machine.

The provided data or file content will be base64-encoded. During provisioning, waagent will store this data on the VM as both an attribute of __/var/lib/waagent/ovf-env.xml__ and as the sole contents of __/var/lib/waagent/CustomData__. By default, waagent will store the data on the VM as it was encoded during transport; the contents will need to be base64-decoded in order to access the original custom data. Waagent can be configured to decode the custom data and write out the original data, by changing the __Provisioning.DecodeCustomData__ attribute in __/etc/waagent.conf__.

Note: customdata is limited to 64K; using a file larger than 64K will fail.

## __--deallocate-resources__

In a shutdown request, shuts down the Virtual Machine and releases the compute resources. You are not billed for the compute resources that this Virtual Machine uses. If a static Virtual Network IP address is assigned to the Virtual Machinethe status of the IP address is changed to become a reserved IP address.

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
