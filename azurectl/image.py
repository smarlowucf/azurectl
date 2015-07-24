# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService
from azure.storage.blob import BlobService

# project
from azurectl_exceptions import (
    AzureOsImageListError,
    AzureBlobServicePropertyError,
    AzureOsImageCreateError,
    AzureOsImageDeleteError
)


class Image(object):
    """
        Implements showing and creation of Azure images from a previously
        uploaded vhd disk image file
    """
    def __init__(self, account):
        self.account = account
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.cert_file = NamedTemporaryFile()
        self.publishsettings = self.account.publishsettings()
        self.cert_file.write(self.publishsettings.private_key)
        self.cert_file.write(self.publishsettings.certificate)
        self.cert_file.flush()

    def list(self):
        result = []
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            for image in service.list_os_images():
                result.append({
                    'name': image.name,
                    'label': image.label,
                    'os': image.os,
                    'category': image.category,
                    'description': image.description,
                    'location': image.location,
                    'affinity_group': image.affinity_group,
                    'media_link': image.media_link
                })
        except Exception as e:
            raise AzureOsImageListError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result

    def create(self, name, blob_name, label=None, container_name=None):
        if not container_name:
            container_name = self.account.storage_container()
        if not label:
            label = name
        try:
            storage = BlobService(self.account_name, self.account_key)
            storage.get_blob_properties(
                container_name, blob_name
            )
        except Exception as e:
            raise AzureBlobServicePropertyError(
                '%s not found in container %s' % (blob_name, container_name)
            )
        try:
            media_link = storage.make_blob_url(container_name, blob_name)
            service = ServiceManagementService(
                self.publishsettings.subscription_id,
                self.cert_file.name
            )
            result = service.add_os_image(
                label, media_link, name, 'Linux'
            )
            return (result.request_id)
        except Exception as e:
            raise AzureOsImageCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def delete(self, name, delete_disk=False):
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            result = service.delete_vm_image(
                name, delete_disk
            )
            return(result.request_id)
        except Exception as e:
            raise AzureOsImageDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )
