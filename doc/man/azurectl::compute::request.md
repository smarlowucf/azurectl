# NAME

azurectl - Command Line Interface to manage Microsoft Azure

Most requests to the Azure API are asynchronous and return only a request ID.

# SYNOPSIS

__azurectl__ compute request status --id=*number*

__azurectl__ compute request wait --id=*number*

# DESCRIPTION

## __status__

Provide status information for the given request number

## __wait__

Wait for a request to complete. A request is completed if the 'Succeeded' status
was received. In case of an error an exception is thrown. The maximum wait
period is set to 300s (5min), after this timeout an AzureRequestTimeout
exception is thrown.

# OPTIONS

## __--id=number__

The request id number. Any task in azurectl which comes back with a request id
information can be used to ask for its status or to wait on request completion.
Please note, not all commands supports request tracking which depends on the
implementation in the
[python-azure-sdk](https://github.com/Azure/azure-sdk-for-python).
