# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute image list

__azurectl__ compute image create --name=*imagename* --blob=*blobname*

    [--container=container]
    [--label=label]

__azurectl__ compute image replicate --name=*imagename* --regions=*regionlist* --offer=*offer* --sku=*sku* --image-version=*version*

__azurectl__ compute image unreplicate --name=*imagename*

__azurectl__ compute image publish --name=*imagename*

    [--private]
    [--msdn]

# DESCRIPTION

## __list__

List registered images and their attributes

## __create__

Register operating system image from a VHD disk stored in a Microsoft Azure blob storage container. Before creating an image, the VHD must be uploaded to storage as a page blob. See the __azurectl compute storage upload__ command

## __replicate__

Replicate a VM image to multiple target locations. This operation is only for publishers. You have to be registered as image publisher with Microsoft Azure to be able to call this.

## __unreplicate__

Unreplicate a VM image from all regions. Like with replication this operation is only for publishers.

## __publish__

Publicly share an already replicated VM image. This operation is only for
publishers. You have to be registered as image publisher with Windows
Azure to be able to call this.

# OPTIONS

## __--container=container__

Select container name. This will overwrite the __storage_container_name__ from the config file

## __--label__

Specify a custom label for the operating system image when calling create If no label is specified the label is equal to the given name

## __--name__

Specify the VM name in an image creation or replication process

## __--blob__

Specify the base filename of the disk image (VHD) as it is stored on the blob storage

## __--regions__

Specify a comma separated list of region names

## __--offer__

Publisher meta data, specifies the name of the offer

## __--sku__

Publisher meta data, specifies the name of the sku

## __--image-version__

Publisher meta data, specifies the semantic version of the image. For details on the format see: http://semver.org. Example: 1.0.0

## __--private__

When publising an image this option limits the scope of the shared image to be account private

## __--msdn__

When publising an image this option limits the scope of the shared image to the Microsoft Developer Network
