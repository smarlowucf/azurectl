# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute endpoint create --cloud-service-name=*name* --name=*name* --port=*port*

    [--instance-name=name]
    [--instance-port=port]
    [--idle-timeout=minutes]
    [--udp]

__azurectl__ compute endpoint show --cloud-service-name=*name* --name=*name*

    [--instance-name=name]

__azurectl__ compute endpoint list --cloud-service-name=*name*

    [--instance-name=name]

__azurectl__ compute endpoint delete --cloud-service-name=*name* --name=*name*

    [--instance-name=name]

# DESCRIPTION

## __create__

Open a new port (endpoint) on a cloud service's network interface, forwarded to
a port on the specified virtual machine instance. If the virtual machine's
__instance-name__ is the same as the __cloud-service-name__, the
__--instance-name__ argument may be omitted.

## __show__

List information about a single endpoint, forwarded to the selected virtual
machine, with the name __name__.

## __list__

List information about all endpoints forwarded to the selected virtual machine.

## __delete__

Close a named endpoint on a cloud service.

# OPTIONS

## __--cloud-service-name=name__

Name of the cloud service where the selected virtual machine may be found.

## __--name=name__

Name of the endpoint, usually the name of the protocol that is carried.

## __--instance-name=name__

Name of the virtual machine instance. If no name is given, the instance name is
assumed to be the same as the __cloud-service-name__.

## __--port=port__

Numbered port to open on the cloud service. All traffic to this port will be
forwarded to the selected virtual machine instance on its __instance-port__.

## __--instance-port=port__

Numbered port on the instance to which traffic will be forward from the __port__
of the cloud-service. If no port is given, the instance port is assumed to be
the same as the cloud service __port__.

## __--idle-timeout=minutes__

Specifies the timeout for the TCP idle connection. The value can be set between
4 and 30 minutes. The default value is 4 minutes.

**Note:** Does not apply to UDP connections.

## __--udp__

Select UDP as the transport protocol for the endpoint. Otherwise, the transport
protocol will be assumed to be TCP.
