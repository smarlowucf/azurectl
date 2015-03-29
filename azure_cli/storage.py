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
from azure.storage import BlobService

# project
from xz import XZ
from azurectl_exceptions import *
from logger import Logger


class Storage:
    """
        Implements storage operations in Azure storage containers
    """
    def __init__(self, account, container):
        self.content_encoding = None
        self.content_language = None
        self.content_md5 = None
        self.cache_control = None
        self.x_ms_blob_content_type = None
        self.x_ms_blob_content_encoding = None
        self.x_ms_blob_content_language = None
        self.x_ms_blob_content_md5 = None
        self.x_ms_blob_cache_control = None
        self.x_ms_meta_name_values = None
        self.x_ms_lease_id = None
        self.x_ms_blob_sequence_number = None

        self.account = account
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.container = container
        self.upload_status = {'current_bytes': 0, 'total_bytes': 0}

    def upload(self, image, name, max_chunk_size=None):
        if not os.path.exists(image):
            raise AzureStorageFileNotFound("File %s not found" % image)
        blob_service = BlobService(self.account_name, self.account_key)
        blob_name = name
        if not blob_name:
            blob_name = os.path.basename(image)

        if not max_chunk_size:
            # BLOB_MAX_CHUNK_DATA_SIZE = 4 MB
            max_chunk_size = blob_service._BLOB_MAX_CHUNK_DATA_SIZE
        max_chunk_size = int(max_chunk_size)

        image_size = XZ.uncompressed_size(image)

        # PageBlob must be 512 byte aligned
        remainder = image_size % 512
        if remainder != 0:
            raise AzurePageBlobAlignmentViolation(
                "Uncompressed size %d is not 512 byte aligned" % image_size
            )

        zero_page = None
        self.__upload_status(0, image_size)
        try:
            with open('/dev/zero', 'rb') as zero_stream:
                zero_page = zero_stream.read(max_chunk_size)
            blob_service.put_blob(
                self.container,
                blob_name,
                None,
                'PageBlob',
                self.content_encoding,
                self.content_language,
                self.content_md5,
                self.cache_control,
                self.x_ms_blob_content_type,
                self.x_ms_blob_content_encoding,
                self.x_ms_blob_content_language,
                self.x_ms_blob_content_md5,
                self.x_ms_blob_cache_control,
                self.x_ms_meta_name_values,
                self.x_ms_lease_id,
                image_size,
                self.x_ms_blob_sequence_number
            )
        except Exception as e:
            raise AzureStorageUploadError('%s (%s)' % (type(e), str(e)))
        try:
            with XZ.open(image) as stream:
                rest_bytes = image_size
                page_start = 0
                while True:
                    requested_bytes = min(
                        rest_bytes, max_chunk_size
                    )
                    if requested_bytes != max_chunk_size:
                        with open('/dev/zero', 'rb') as zero_stream:
                            zero_page = zero_stream.read(requested_bytes)
                    data = stream.read(requested_bytes)
                    if data:
                        length = len(data)
                        rest_bytes -= length
                        page_end = page_start + length - 1
                        if not data == zero_page:
                            blob_service.put_page(
                                self.container,
                                blob_name,
                                data,
                                'bytes={0}-{1}'.format(page_start, page_end),
                                'update',
                                x_ms_lease_id=None
                            )
                        page_start += length
                        self.__upload_status(
                            page_start, image_size
                        )
                    else:
                        self.__upload_status(
                            image_size, image_size
                        )
                        break
        except Exception as e:
            raise AzureStorageUploadError('%s (%s)' % (type(e), str(e)))

    def delete(self, image):
        blob_service = BlobService(self.account_name, self.account_key)
        try:
            blob_service.delete_blob(self.container, image)
        except Exception as e:
            raise AzureStorageDeleteError('%s (%s)' % (type(e), str(e)))

    def print_upload_status(self):
        Logger.progress(
            self.upload_status['current_bytes'],
            self.upload_status['total_bytes'],
            'Uploading'
        )

    def __upload_status(self, current, total):
        self.upload_status['current_bytes'] = current
        self.upload_status['total_bytes'] = total
