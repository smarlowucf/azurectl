# NAME

azurectl - Command Line Interface to manage Microsoft Azure

# SYNOPSIS

__azurectl__ compute image list

__azurectl__ compute image show --name=*imagename*

__azurectl__ compute image create --name=*imagename* --blob-name=*blobname*

    [--label=label]

__azurectl__ compute image replicate --name=*imagename* --regions=*regionlist* --offer=*offer* --sku=*sku* --image-version=*version*

__azurectl__ compute image unreplicate --name=*imagename*

__azurectl__ compute image publish --name=*imagename*

    [--private]
    [--msdn]

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

# DESCRIPTION

## __list__

List registered images and their attributes

##__show__

List information about a single image

## __create__

Register operating system image from a VHD disk stored in a Microsoft Azure blob storage container. Before creating an image, the VHD must be uploaded to storage as a page blob. See the __azurectl compute storage upload__ command

## __replicate__

Replicate a VM image to multiple target locations. This operation is only for publishers. You have to be registered as image publisher with Microsoft Azure to be able to call this. If the region name __all__ is provided, azurectl will replicate to all regions that are valid for your subscription.

## __unreplicate__

Unreplicate a VM image from all regions. Like with replication this operation is only for publishers.

## __publish__

Publicly share an already replicated VM image. This operation is only for publishers. You have to be registered as image publisher with Windows Azure to be able to call this.

## __update__

Update OS image metadata. Every image in the storage repository contains a set of metadata information describing the image more detailed. The __azurectl compute image list__ command prints this information for every image in the repository matching the account setup. With the update command some of the elements can be changed. Please be aware, publisher data like eula, image-family or published-date can only be changed with an account registered as image publisher with Microsoft Azure.

# OPTIONS

## __--label__

Specify a custom label for the operating system image when calling create If no label is specified the label is equal to the given name

## __--name__

Specify the VM name in an image creation or replication process

## __--blob-name__

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

## __--description__

A long-format text description of the image.

## __--eula__

An URL where an end-user may read the text of the images end user license agreement.

## __--image-family__

An arbitrary classification of the image, in order to categorize versions of an image in the Azure gallery; this is replaced by a combination of offer and sku in the Azure marketplace.

## __--icon-uri__

The location to a 100x100px image file referenced by one of the following capabilities:

* The name of the image file local to the Azure gallery.
* The URL of the image to use as a large icon in the Azure gallery list.

## __--label__

A one-line __title__ for the image.

## __--language__

The language the OS image is configured with. We recommend the standard country code format, e.g __en_US__

## __--privacy-uri__

An URL where an end-user may read the privacy policy that governs information.

## __--published-date__

The date an appliance is published, in the format __yyyy-mm-dd__.

## __--small-icon-uri__

The location to a 45x45px image file referenced by one of the following capabilities:

* The name of the image file local to the Azure gallery.
* The URL of the image to use as a small icon in the Azure gallery list.
