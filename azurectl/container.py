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
from azure.storage.blob import BlobService
from azure.storage import (
    AccessPolicy,
    SharedAccessPolicy,
    SharedAccessSignature
)
from azure.storage.sharedaccesssignature import (
    ResourceType
)

# project
from azurectl_exceptions import (
    AzureContainerListError,
    AzureContainerListContentError
)

ISO8061_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Container(object):
    """
        Information from Azure storage containers
    """
    def __init__(self, account):
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.blob_service_host_base = account.get_blob_service_host_base()

    def list(self):
        result = []
        blob_service = BlobService(self.account_name, self.account_key,
                                   host_base=self.blob_service_host_base)
        try:
            for container in blob_service.list_containers():
                result.append(format(container.name))
        except Exception as e:
            raise AzureContainerListError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result

    def content(self, container):
        result = {container: []}
        blob_service = BlobService(self.account_name, self.account_key,
                                   host_base=self.blob_service_host_base)
        try:
            for blob in blob_service.list_blobs(container):
                result[container].append(format(blob.name))
            return result
        except Exception as e:
            raise AzureContainerListContentError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def sas(self, container, start, expiry, permissions):
        sap = SharedAccessPolicy(AccessPolicy(
            start.strftime(ISO8061_FORMAT),
            expiry.strftime(ISO8061_FORMAT),
            permissions
        ))

        sas = SharedAccessSignature(self.account_name, self.account_key)
        signed_query = sas.generate_signed_query_string(
            container,
            ResourceType.RESOURCE_CONTAINER,
            sap
        )
        return 'https://{}.blob.core.windows.net/{}?{}'.format(
            self.account_name, container, signed_query
        )
