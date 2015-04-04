# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute storage upload --source=*xzfile* --name=*blobname*
__azurectl__ compute storage delete --name=*blobname*

# DESCRIPTION

## __upload__

Upload an XZ compressed file to a container. While any kind of data can be uploaded to the blob storage the purpose of this command is mainly for uploading VHD (Virtual Hard Drive) disk images in order to register an Azure operating system image from it at a later point in time

## __delete__

Delete a file from a container

# OPTIONS

## __--container=container__

Select container name. This will overwrite the __storage_container_name__ from the config file

## __--max-chunk-size=byte_size__

Specify the maximum page size for uploading data. By default a page size of 4MB is used

## __--quiet__

Suppress progress information on upload
