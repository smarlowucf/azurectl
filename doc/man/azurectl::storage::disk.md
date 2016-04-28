# NAME

azurectl - Command Line Interface to manage Microsoft Azure

In order to make use of a disk image in Azure, a fixed-size virtual hard disk
(VHD) file must be uploaded to storage as a page blob.

# SYNOPSIS

__azurectl__ storage disk upload --source=*file*

    [--blob-name=<blobname>]
    [--max-chunk-size=<size>]
    [--quiet]

__azurectl__ storage disk delete --name=*blobname*

# DESCRIPTION

## __upload__

Upload file to a page blob in a container. The command autodetects the filetype
whether it is XZ-compressed or not and decompresses the image automatically. If
the filetype could not be identified the file will be uploaded as raw sequence
of bytes.

While any kind of data can be uploaded to the blob storage the purpose of this
command is mainly for uploading XZ-compressed VHD (Virtual Hard Drive) disk
images in order to register an Azure operating system image from it at a later
point in time.

## __delete__

Delete a file from a container.

# OPTIONS

## __--blob-name=blobname__

Name of the uploaded file in the storage pool. If not specified the name
is the same as the file used for upload.

## __--max-chunk-size=byte_size__

Specify the maximum page size for uploading data. By default a page size of 4MB
is used.

## __--quiet__

Suppress progress information on upload.
