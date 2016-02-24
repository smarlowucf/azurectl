# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute reserved-ip list

__azurectl__ compute reserved-ip show --name=*reserved_ip_name*

__azurectl__ compute reserved-ip create --name=*reserved_ip_name*

__azurectl__ compute reserved-ip delete --name=*reserved_ip_name*


# DESCRIPTION

## __list__

List IP addresses reserved within this account.

##__show__

List information about a single IP address reservation.

## __create__

Add a new IP address reservation in the default or specified region
(use the global --region argument).

## __delete__

Release a reserved IP address.

# OPTIONS

## __--name__

Specify a convenient name for identifying a specific IP address reservation.
