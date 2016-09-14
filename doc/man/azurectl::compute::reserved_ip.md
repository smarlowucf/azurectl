# NAME

azurectl - Command Line Interface to manage Microsoft Azure

In order to maintain access to a specific public IP address, a reservation can be made. Reservations are identified by a user-defined name.

# SYNOPSIS

__azurectl__ compute reserved-ip create --name=*reserved_ip_name*

   [--wait]

__azurectl__ compute reserved-ip list

__azurectl__ compute reserved-ip show --name=*reserved_ip_name*

__azurectl__ compute reserved-ip delete --name=*reserved_ip_name*

   [--wait]

__azurectl__ compute reserved-ip associate --name=*reserved-ip-name* --cloud-service-name=*name*

   [--wait]

__azurectl__ compute reserved-ip disassociate --name=*reserved-ip-name* --cloud-service-name=*name*

   [--wait]


# DESCRIPTION

## __associate__

Associate an existing reserved IP address to a deployment

## __disassociate__

Disassociate an existing reserved IP address from the given deployment

## __create__

Add a new IP address reservation in the default or specified region (use the global --region argument).

## __delete__

Release a reserved IP address.

## __list__

List IP addresses reserved within this account.

##__show__

List information about a single IP address reservation.

# OPTIONS

## __--cloud-service-name=*name*__

Name of the cloud service to use for associate or disassociate a reserved IP address

## __--name__

Specify a convenient name for identifying a specific IP address reservation.

## __--wait__

wait for the request to change its status to succeeded
