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
import collections
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService
from azure.storage.blob import BlobService

# project
from azurectl_exceptions import (
    AzureOsImageListError,
    AzureOsImageShowError,
    AzureBlobServicePropertyError,
    AzureOsImageCreateError,
    AzureOsImageDeleteError,
    AzureOsImageReplicateError,
    AzureOsImageUnReplicateError,
    AzureOsImagePublishError,
    AzureOsImageUpdateError
)
from defaults import Defaults


class Image(object):
    """
        Implements Azure image management from a previously uploaded
        vhd disk image file. This includes the following task
        + creation and deletion of VM images
        + replication of VM images to multiple regions
        + listing VM images
        + publish VM images
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

    def _decorate_image_for_results(self, image):
        return {
            'affinity_group': image.affinity_group,
            'category': image.category,
            'description': image.description,
            'eula': image.eula,
            'icon_uri': image.icon_uri,
            'image_family': image.image_family,
            'is_premium': image.is_premium,
            'label': image.label,
            'language': image.language,
            'location': image.location,
            'logical_size_in_gb': image.logical_size_in_gb,
            'media_link': image.media_link,
            'name': image.name,
            'os': image.os,
            'os_state': image.os_state,
            'pricing_detail_link': image.pricing_detail_link,
            'privacy_uri': image.privacy_uri,
            'published_date': image.published_date,
            'publisher_name': image.publisher_name,
            'recommended_vm_size': image.recommended_vm_size,
            'show_in_gui': image.show_in_gui,
            'small_icon_uri': image.small_icon_uri
        }

    def list(self):
        result = []
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            for image in service.list_os_images():
                result.append(self._decorate_image_for_results(image))
        except Exception as e:
            raise AzureOsImageListError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result

    def show(self, name):
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            image = service.get_os_image(name)
        except Exception as e:
            raise AzureOsImageShowError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return self._decorate_image_for_results(image)

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
            result = service.delete_os_image(
                name, delete_disk
            )
            return(result.request_id)
        except Exception as e:
            raise AzureOsImageDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def update(self, image_name, update_record):
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            os_image = service.get_os_image(image_name)
        except Exception as e:
            raise AzureOsImageUpdateError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        os_image_attributes = [
            'description',
            'eula',
            'icon_uri',
            'image_family',
            'label',
            'language',
            'privacy_uri',
            'published_date',
            'small_icon_uri'
        ]
        ordered_record = collections.OrderedDict(
            sorted(update_record.items())
        )
        for name, value in ordered_record.iteritems():
            if value is not None:
                Defaults.set_attribute(os_image, name, value)
        try:
            service.update_os_image_from_image_reference(
                image_name, os_image
            )
            os_image_updated = service.get_os_image(
                image_name
            )
        except Exception as e:
            raise AzureOsImageUpdateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

        elements_not_changed = []
        for name in os_image_attributes:
            value_desired = Defaults.get_attribute(os_image, name)
            value_current = Defaults.get_attribute(os_image_updated, name)
            if value_desired != value_current:
                elements_not_changed.append(name)
        if elements_not_changed:
            message = [
                'The element(s) "%s" could not be updated.' %
                ','.join(elements_not_changed),
                'Please check if your account is registered as image publisher'
            ]
            raise AzureOsImageUpdateError(
                ' '.join(message)
            )

    def replicate(self, name, regions, offer, sku, version):
        '''
        Note: The regions are not additive. If a VM Image has already
        been replicated to Regions A, B, and C, and a request is made
        to replicate to Regions A and D, the VM Image will remain in
        Region A, will be replicated in Region D, and will be
        unreplicated from Regions B and C
        '''
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        if 'all' in regions:
            regions = []
            for location in service.list_locations():
                regions.append(location.name)
        try:
            result = service.replicate_vm_image(
                name, regions, offer, sku, version
            )
            return(result.request_id)
        except Exception as e:
            raise AzureOsImageReplicateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def unreplicate(self, name):
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            result = service.unreplicate_vm_image(name)
            return(result.request_id)
        except Exception as e:
            raise AzureOsImageUnReplicateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def publish(self, name, permission):
        service = ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name
        )
        try:
            result = service.share_vm_image(name, permission)
            return(result.request_id)
        except Exception as e:
            raise AzureOsImagePublishError(
                '%s: %s' % (type(e).__name__, format(e))
            )
