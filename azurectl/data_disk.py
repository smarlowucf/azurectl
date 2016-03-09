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
from datetime import datetime
# project
from service_manager import *


class DataDisk(ServiceManager):
    """
        Implements virtual machine data disk (non-root/boot disk) management.
    """

    def create(
        self,
        cloud_service_name,
        instance_name,
        size,
        lun=None,
        host_caching=None,
        filename=None,
        label=None,
        role_name=None
    ):
        if lun not in range(16):
            lun = self.get_first_available_lun(
                cloud_service_name,
                instance_name,
                role_name=role_name
            )
        args = {
            'media_link': self.__data_disk_url(
                filename or self.generate_filename(instance_name)
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
                instance_name,
                (role_name or cloud_service_name),
                lun,
                **args
            )
        except Exception as e:
            raise AzureDataDiskCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result.request_id

    def get_first_available_lun(
        self,
        cloud_service_name,
        instance_name,
        role_name=None
    ):
        lun = 0
        while lun < 16:  # 15 is the max lun
            try:
                self.service.get_data_disk(
                    cloud_service_name,
                    instance_name,
                    (role_name or cloud_service_name),
                    lun
                )
            except AzureMissingResourceHttpError:
                return lun
            else:
                lun += 1
        raise AzureDataDiskNoAvailableLun(
            "All LUNs on this VM are occupied."
        )

    def generate_filename(self, instance_name):
        return '%s-data-disk-%s.vhd' % (
            instance_name,
            datetime.isoformat(datetime.utcnow())
        )

    def __data_disk_url(self, filename):
        return (
            'https://' +
            self.account_name +
            '.blob.' +
            self.account.get_blob_service_host_base() + '/' +
            self.account.storage_container() + '/' +
            filename
        )
