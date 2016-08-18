# Copyright (c) 2016 SUSE.  All rights reserved.
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
from azure.common import AzureMissingResourceHttpError
from azure.storage.blob.pageblobservice import PageBlobService
from datetime import datetime

# project
from ..defaults import Defaults

from ..azurectl_exceptions import (
    AzureDataDiskCreateError,
    AzureDataDiskShowError,
    AzureDataDiskDeleteError,
    AzureDataDiskNoAvailableLun
)


class DataDisk(object):
    """
        Implements virtual machine data disk (non-root/boot disk) management.
    """
    def __init__(self, account):
        self.account = account
        self.service = account.get_management_service()
        self.data_disk_name = None

    def create(
        self,
        size,
        cloud_service_name,
        instance_name=None,
        lun=None,
        host_caching=None,
        filename=None,
        label=None
    ):
        """
            Create and attach a new data disk to the specified
            virtual machine at the optionally specified lun
        """
        if not instance_name:
            instance_name = cloud_service_name

        if lun not in range(16):
            lun = self.__get_first_available_lun(
                cloud_service_name, instance_name
            )
        args = {
            'media_link': self.__data_disk_url(
                filename or self.__generate_filename(instance_name)
            ),
            'logical_disk_size_in_gb': size
        }
        if host_caching:
            args['host_caching'] = host_caching
        if label:
            args['disk_label'] = label
        try:
            result = self.service.add_data_disk(
                cloud_service_name,
                cloud_service_name,
                instance_name,
                lun,
                **args
            )
        except Exception as e:
            raise AzureDataDiskCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result.request_id

    def show(self, disk_name):
        """
            Show details of the specified disk
        """
        try:
            disk = self.service.get_disk(disk_name)
        except Exception as e:
            raise AzureDataDiskShowError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return self.__decorate_disk(disk)

    def delete(self, disk_name):
        """
            Delete data disk and the underlying vhd disk image
            Note the deletion will fail if the disk is still
            in use, meaning attached to an instance
        """
        try:
            self.service.delete_disk(disk_name, delete_vhd=True)
        except Exception as e:
            raise AzureDataDiskDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def list(self):
        """
            List disk(s) from your image repository
        """
        disks = []
        try:
            disks = self.service.list_disks()
        except Exception:
            pass
        return [
            self.__decorate_disk_list(disk) for disk in disks
        ]

    def show_attached(
        self, cloud_service_name, instance_name=None, at_lun=None
    ):
        """
            Show details of the data disks attached to the virtual
            machine. If a lun is specified show only details for the disk
            at the specified lun
        """
        if not instance_name:
            instance_name = cloud_service_name

        disks = []
        luns = [at_lun] if at_lun is not None else range(Defaults.max_vm_luns())
        for lun in luns:
            try:
                disks.append(self.service.get_data_disk(
                    cloud_service_name, cloud_service_name, instance_name, lun
                ))
            except Exception as e:
                if at_lun is not None:
                    # only if a disk information is requested for a specific
                    # lun but does not exist, an exception is raised
                    raise AzureDataDiskShowError(
                        '%s: %s' % (type(e).__name__, format(e))
                    )
        return [self.__decorate_attached_disk(disk) for disk in disks]

    def attach(
        self, disk_name, cloud_service_name, instance_name=None,
        label=None, lun=None, host_caching=None
    ):
        """
            Attach existing data disk to the instance
        """
        disk_url = self.__data_disk_url(disk_name + '.vhd')

        if not instance_name:
            instance_name = cloud_service_name

        if lun not in range(Defaults.max_vm_luns()):
            lun = self.__get_first_available_lun(
                cloud_service_name, instance_name
            )

        args = {
            'media_link': disk_url,
            'disk_name': disk_name
        }
        if host_caching:
            args['host_caching'] = host_caching
        if label:
            args['disk_label'] = label

        try:
            result = self.service.add_data_disk(
                cloud_service_name, cloud_service_name, instance_name, lun,
                **args
            )
            self.attached_lun = lun
        except Exception as e:
            raise AzureDataDiskCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result.request_id

    def detach(self, lun, cloud_service_name, instance_name=None):
        """
            Delete data disk from the instance, retaining underlying vhd blob
        """
        if not instance_name:
            instance_name = cloud_service_name

        try:
            result = self.service.delete_data_disk(
                cloud_service_name, cloud_service_name, instance_name, lun,
                delete_vhd=False
            )
        except Exception as e:
            raise AzureDataDiskDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result.request_id

    def __get_first_available_lun(self, cloud_service_name, instance_name):
        lun = 0
        while lun < Defaults.max_vm_luns():
            try:
                self.service.get_data_disk(
                    cloud_service_name, cloud_service_name, instance_name, lun
                )
            except AzureMissingResourceHttpError:
                return lun
            else:
                lun += 1
        raise AzureDataDiskNoAvailableLun(
            "All LUNs on this VM are occupied."
        )

    def __generate_filename(self, identifier):
        """
            Generate vhd disk name with respect to the Azure naming
            conventions for data disks
        """
        self.data_disk_name = '%s-data-disk-%s.vhd' % (
            identifier, datetime.isoformat(datetime.utcnow()).replace(':', '_')
        )
        return self.data_disk_name

    def __data_disk_url(self, filename):
        blob_service = PageBlobService(
            self.account.storage_name(),
            self.account.storage_key(),
            endpoint_suffix=self.account.get_blob_service_host_base()
        )
        return blob_service.make_blob_url(
            self.account.storage_container(),
            filename
        )

    def __decorate_attached_disk(self, data_virtual_hard_disk):
        return {
            'label': data_virtual_hard_disk.disk_label,
            'host-caching': data_virtual_hard_disk.host_caching,
            'disk-url': data_virtual_hard_disk.media_link,
            'source-image-url': data_virtual_hard_disk.source_media_link,
            'lun': data_virtual_hard_disk.lun,
            'size': '%d GB' % data_virtual_hard_disk.logical_disk_size_in_gb
        }

    def __decorate_disk(self, disk):
        attach_info = {}
        if disk.attached_to:
            attach_info = {
                'hosted_service_name': disk.attached_to.hosted_service_name,
                'deployment_name': disk.attached_to.deployment_name,
                'role_name': disk.attached_to.role_name
            }
        return {
            'affinity_group': disk.affinity_group,
            'attached_to': attach_info,
            'has_operating_system': disk.has_operating_system,
            'is_corrupted': disk.is_corrupted,
            'location': disk.location,
            'logical_disk_size_in_gb': '%d GB' % disk.logical_disk_size_in_gb,
            'label': disk.label,
            'media_link': disk.media_link,
            'name': disk.name,
            'os': disk.os,
            'source_image_name': disk.source_image_name
        }

    def __decorate_disk_list(self, disk):
        attached = True if disk.attached_to else False
        return {
            'is_attached': attached,
            'name': disk.name,
        }
