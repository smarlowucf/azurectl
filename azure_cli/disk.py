# core
import os

# extensions
from azure.storage import BlobService

# project
from exceptions import *
from logger import Logger

class Disk:
    def __init__(self, storage_account, container):
        self.content_encoding           = None
        self.content_language           = None
        self.content_md5                = None
        self.cache_control              = None
        self.x_ms_blob_content_type     = None
        self.x_ms_blob_content_encoding = None
        self.x_ms_blob_content_language = None
        self.x_ms_blob_content_md5      = None
        self.x_ms_blob_cache_control    = None
        self.x_ms_meta_name_values      = None
        self.x_ms_lease_id              = None
        self.account_name = storage_account.get_name()
        self.account_key  = storage_account.get_key()
        self.container    = container
        self.upload_status = {'current_bytes': 0, 'total_bytes': 0}

    def upload(self, image, max_data_size=None, max_chunk_size=None):
        if not os.path.exists(image):
            raise AzureDiskImageNotFound("Image file %s not found" % image)
        blob_service = BlobService(self.account_name, self.account_key)
        blob_name = os.path.basename(image)

        if not max_data_size:
            # BLOB_MAX_DATA_SIZE = 64 MB
            max_data_size = blob_service._BLOB_MAX_DATA_SIZE
        if not max_chunk_size:
            # BLOB_MAX_CHUNK_DATA_SIZE = 4 MB
            max_chunk_size = blob_service._BLOB_MAX_CHUNK_DATA_SIZE

        max_data_size  = int(max_data_size)
        max_chunk_size = int(max_chunk_size)

        image_size = os.path.getsize(image)
        self.__upload_status(0, image_size)

        try:
            with open(image, 'rb') as stream:
                if image_size < max_data_size:
                    # upload one BLOB_MAX_DATA_SIZE block
                    data = stream.read(image_size)
                    self.__put_blob(
                        blob_service,
                        self.container, blob_name, data
                    )
                    self.__upload_status(image_size, image_size)
                else:
                    # divide by blocks and upload a block list
                    remaining_bytes = image_size
                    bytes_uploaded  = 0
                    block_index     = 0
                    block_ids       = []
                    while True:
                        requested_bytes = min(
                            remaining_bytes, max_chunk_size
                        )
                        data = stream.read(requested_bytes)
                        if data:
                            length = len(data)
                            remaining_bytes -= length
                            block_id = '{0:08d}'.format(block_index)
                            self.__put_block(
                                blob_service,
                                self.container, blob_name, data, block_id
                            )
                            bytes_uploaded += length
                            block_ids.append(block_id)
                            block_index += 1
                            self.__upload_status(
                                bytes_uploaded, image_size
                            )
                        else:
                            break
                    self.__put_block_list(
                        blob_service,
                        container_name, blob_name, block_ids
                    )
        except Exception as e:
            raise AzureDiskUploadError('%s (%s)' %(type(e), str(e)))

    def delete(self, image):
        blob_service = BlobService(self.account_name, self.account_key)
        try:
            blob_service.delete_blob(self.container, image)
        except Exception as e:
            raise AzureDiskDeleteError('%s (%s)' %(type(e), str(e)))

    def print_upload_status(self):
        Logger.info(self.upload_status)

    def __upload_status(self, current, total):
        self.upload_status['current_bytes'] = current
        self.upload_status['total_bytes'] = total

    def __put_blob(self, blob_service, container_name, blob_name, data):
        blob_service.put_blob(
            container_name,
            blob_name,
            data,
            'BlockBlob',
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
            self.x_ms_lease_id
        )

    def __put_block(self, blob_service, container_name, blob_name, data, b_id):
        blob_service.put_block(
            container_name,
            blob_name,
            data,
            b_id,
            x_ms_lease_id = self.x_ms_lease_id
        )

    def __put_block_list(self, blob_service, container_name, blob_name, b_ids):
        blob_service.put_block_list(
            container_name,
            blob_name,
            b_ids,
            self.content_md5,
            self.x_ms_blob_cache_control,
            self.x_ms_blob_content_type,
            self.x_ms_blob_content_encoding,
            self.x_ms_blob_content_language,
            self.x_ms_blob_content_md5,
            self.x_ms_meta_name_values,
            self.x_ms_lease_id
        )
