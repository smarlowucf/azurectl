# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute storage upload --source=*file* --name=*blobname*
__azurectl__ compute storage delete --name=*blobname*

# DESCRIPTION

## __upload__

Upload file to a container. The command autodetects the filetype whether it is compressed or not and applies the appropriate decompressor. If the filetype could not be identified the file will be uploaded as raw sequence of bytes

While any kind of data can be uploaded to the blob storage the purpose of this command is mainly for uploading XZ compressed VHD (Virtual Hard Drive) disk images in order to register an Azure operating system image from it at a later point in time.

## __delete__

Delete a file from a container

# OPTIONS

## __--container=container__

Select container name. This will overwrite the __storage_container_name__ from the config file

## __--max-chunk-size=byte_size__

Specify the maximum page size for uploading data. By default a page size of 4MB is used

## __--quiet__

Suppress progress information on upload
