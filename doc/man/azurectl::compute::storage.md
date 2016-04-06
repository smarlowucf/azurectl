# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute storage upload --source=*file*

    [--name=<blobname>]
    [--max-chunk-size=<size>]
    [--quiet]

__azurectl__ compute storage delete --name=*blobname*

# DESCRIPTION

## __upload__

Upload file to a page blob in a container. The command autodetects the filetype whether it is XZ-compressed or not and decompresses the image automatically. If the filetype could not be identified the file will be uploaded as raw sequence of bytes.

While any kind of data can be uploaded to the blob storage the purpose of this command is mainly for uploading XZ-compressed VHD (Virtual Hard Drive) disk images in order to register an Azure operating system image from it at a later point in time.

## __delete__

Delete a file from a container

# OPTIONS

## __--name=blobname__

Name of the uploaded file in the storage pool. If not specified the name
is the same as the file used for upload

## __--max-chunk-size=byte_size__

Specify the maximum page size for uploading data. By default a page size of 4MB is used

## __--quiet__

Suppress progress information on upload
