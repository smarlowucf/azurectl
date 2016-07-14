# NAME

azurectl - Command Line Interface to manage Microsoft Azure

Operating System Images are the basis of virtual machines, and are backed by
a fixed virtual hard disk (VHD) image in blob storage.

# SYNOPSIS

__azurectl__ compute image create --name=*imagename* --blob-name=*blobname*

    [--label=label]
    [--wait]

__azurectl__ compute image replicate --name=*imagename* --regions=*regionlist*
--offer=*offer* --sku=*sku* --image-version=*version*

    [--wait]
    [--quiet]

__azurectl__ compute image list

__azurectl__ compute image replication-status --name=*imagename*

__azurectl__ compute image show --name=*imagename*

__azurectl__ compute image update --name=*imagename*

    [--description=description]
    [--eula=eula]
    [--image-family=image_family]
    [--icon-uri=icon_uri]
    [--label=label]
    [--language=language]
    [--privacy-uri=privacy_uri]
    [--published-date=date]
    [--small-icon-uri=small_icon_uri]

__azurectl__ compute image publish --name=*imagename*

    [--private]
    [--msdn]
    [--wait]

__azurectl__ compute image delete --name=*imagename*

    [--wait]

__azurectl__ compute image unreplicate --name=*imagename*

# DESCRIPTION

## __create__

Register operating system image from a VHD disk stored in a Microsoft Azure blob storage container. Before creating an image, the VHD must be uploaded to storage as a page blob. See the __azurectl storage disk upload__ command.

## __delete__

Deregister an operating system image. By default, the backing VHD file will be kept in storage, but With the __--delete-disk__ option, the file will be deleted from the storage as well.

## __list__

List registered images and their attributes

## __show__

List information about a single image

## __publish__

Publicly share an already replicated VM image. This operation is only for publishers. You have to be registered as image publisher with Microsoft Azure to be able to call this.

## __replicate__

Replicate a VM image to multiple target locations. This operation is only for publishers. You have to be registered as image publisher with Microsoft Azure to be able to call this. If the region name __all__ is provided, azurectl will replicate to all regions that are valid for your subscription.

## __replication-status__

Show a list of regions a specified image is replicated to, and the completion percentage of the replication operation to each region. When all regions show 100% replication progress, the image is completely replicated.

## __unreplicate__

Unreplicate a VM image from all regions. Like replication, this operation is only for publishers.

## __update__

Update OS image metadata. Every image in the storage repository contains a set of metadata information describing the image more detailed. The __azurectl compute image list__ command prints this information for every image in the repository matching the account setup. With the update command some of the elements can be changed. Please be aware, publisher data like eula, image-family or published-date can only be changed with an account registered as image publisher with Microsoft Azure.

# OPTIONS

## __--blob-name__

Specify the base filename of the disk image (VHD) as it is stored on the blob storage.

## __--delete-disk__

When deleting an image, forces the deletion of the backing VHD file from storage
as well. Without specifying this option with __azurectl compute image delete__, the blob will remain in storage.

## __--description__

A long-format text description of the image.

## __--eula__

An URL where an end-user may read the text of the images end user license
agreement.

## __--icon-uri__

The location to a 100x100px image file referenced by one of the following capabilities:

* The name of the image file local to the Azure gallery.
* The URL of the image to use as a large icon in the Azure gallery list.

## __--image-family__

An arbitrary classification of the image, in order to categorize versions of an image in the Azure gallery; this is replaced by a combination of offer and sku in the Azure marketplace.

## __--image-version__

Publisher meta data, specifies the semantic version of the image. For details on
the format see: http://semver.org. Example: 1.0.0

## __--label__

Specify a custom label for the operating system image when calling create If no label is specified the label is equal to the given name.

## __--language__

The language the OS image is configured with. We recommend the standard country code format, e.g __en_US__.

## __--msdn__

When publising an image this option limits the scope of the shared image to the Microsoft Developer Network.

## __--name__

Specify the VM name in an image creation or replication process

## __--offer__

Publisher meta data, specifies the name of the offer.

## __--privacy-uri__

An URL where an end-user may read the privacy policy that governs information.

## __--private__

When publising an image this option limits the scope of the shared image to be account private.

## __--published-date__

The date an appliance is published, in the format __yyyy-mm-dd__.

## __--quiet__

Suppress progress information during long-running processes, such as when running __azurectl compute storage replicate__ with the __--wait__ option.

## __--regions__

Specify a comma separated list of region names

## __--sku__

Publisher meta data, specifies the name of the sku

## __--small-icon-uri__

The location to a 45x45px image file referenced by one of the following capabilities:

* The name of the image file local to the Azure gallery.
* The URL of the image to use as a small icon in the Azure gallery list.

## __--wait__

wait for the request to change its status to succeeded. On replication
delay the completion of azurectl execution until the replication task
has been completed in the Azure framework.

