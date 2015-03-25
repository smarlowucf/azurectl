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
from azure.storage import BlobService

# project
from azurectl_exceptions import *
from logger import Logger


class Container:
    """
        Information from Azure storage containers
    """
    def __init__(self, account):
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()

    def list(self):
        result = []
        blob_service = BlobService(self.account_name, self.account_key)
        try:
            for container in blob_service.list_containers():
                result.append(str(container.name))
        except Exception as e:
            raise AzureContainerListError('%s (%s)' % (type(e), str(e)))
        return result

    def content(self, container):
        result = {container: []}
        blob_service = BlobService(self.account_name, self.account_key)
        try:
            for blob in blob_service.list_blobs(container):
                result[container].append(str(blob.name))
            return result
        except Exception as e:
            raise AzureContainerListContentError('%s (%s)' % (type(e), str(e)))
