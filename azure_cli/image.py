# Copyright (c) SUSE Linux GmbH.  All rights reserved.
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

# project
from azurectl_exceptions import *
from logger import Logger


class Image:
    """
        Implements showing and creation of Azure images from a previously
        uploaded vhd disk image file
    """
    def __init__(self, account):
        self.account = account

    def list(self):
        result = []
        cert_file = NamedTemporaryFile()
        publishsettings = self.account.publishsettings()
        cert_file.write(publishsettings.private_key)
        cert_file.write(publishsettings.certificate)
        cert_file.flush()
        service = ServiceManagementService(
            publishsettings.subscription_id,
            cert_file.name
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
            raise AzureOsImageListError('%s (%s)' % (type(e), str(e)))
        return result
