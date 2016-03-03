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
import os
from azure.storage.blob.blockblobservice import BlockBlobService

# project
from xz import XZ
from azurectl_exceptions import (
    AzureStorageFileNotFound,
    AzureStorageStreamError,
    AzureStorageUploadError,
    AzureStorageDeleteError,
    AzurePageBlobAlignmentViolation
)
from filetype import FileType
from logger import log


class Storage(object):
    """
        Implements storage operations in Azure storage containers
    """
    def __init__(self, account, container):
        self.account = account
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.blob_service_host_base = self.account.get_blob_service_host_base()
        self.container = container
        self.upload_status = {'current_bytes': 0, 'total_bytes': 0}

    def upload(self, image, name=None, max_chunk_size=None, max_attempts=5):
        if not os.path.exists(image):
            raise AzureStorageFileNotFound('File %s not found' % image)

        blob_name = name
        if not blob_name:
            blob_name = os.path.basename(image)

        image_type = FileType(image)
        image_size = self.__upload_byte_size(
            image, image_type
        )
        self.__validate_page_alignment(image_size)

        try:
            stream = self.__open_upload_stream(image, image_type)
        except Exception as e:
            raise AzureStorageStreamError(
                '%s: %s' % (type(e).__name__, format(e))
            )

        try:
            blob_service = BlockBlobService(
                self.account_name,
                self.account_key,
                endpoint_suffix=self.blob_service_host_base
            )
            if max_chunk_size:
                blob_service.MAX_BLOCK_SIZE = int(max_chunk_size)

            blob_service.create_blob_from_stream(
                container_name=self.container,
                blob_name=blob_name,
                stream=stream,
                count=image_size,
                max_retries=max_attempts,
                progress_callback=self.__upload_status
            )
        except Exception as e:
            stream.close()
            raise AzureStorageUploadError(
                '%s: %s' % (type(e).__name__, format(e))
            )

        stream.close()

    def delete(self, image):
        blob_service = BlockBlobService(
            self.account_name,
            self.account_key,
            endpoint_suffix=self.blob_service_host_base
        )
        try:
            blob_service.delete_blob(self.container, image)
        except Exception as e:
            raise AzureStorageDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def print_upload_status(self):
        log.progress(
            self.upload_status['current_bytes'],
            self.upload_status['total_bytes'],
            'Uploading'
        )

    def __upload_status(self, current, total):
        self.upload_status['current_bytes'] = current
        self.upload_status['total_bytes'] = total

    def __open_upload_stream(self, image, image_type):
        if image_type.is_xz():
            return XZ.open(image)
        return open(image)

    def __upload_byte_size(self, image, image_type):
        if image_type.is_xz():
            return XZ.uncompressed_size(image)
        return os.path.getsize(image)

    def __validate_page_alignment(self, byte_size):
        remainder = byte_size % 512
        if remainder != 0:
            raise AzurePageBlobAlignmentViolation(
                'Uncompressed size %d is not 512 byte aligned' % byte_size
            )
