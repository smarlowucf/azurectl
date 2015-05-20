# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute image list

__azurectl__ compute image create --name=*imagename* --blob=*blobname*

    [--container=container]
    [--label=label]


# DESCRIPTION

## __list__

List registered images and their attributes

## __create__

Register operating system image from a VHD disk stored in a Microsoft Azure blob storage container. Before creating an image, the VHD must be uploaded to storage as a page blob. See the __azurectl compute storage upload__ command

# OPTIONS

## __--container=container__

Select container name. This will overwrite the __storage_container_name__ from the config file

## __--label__

Specify a custom label for the operating system image when calling create If no label is specified the label is equal to the given name
