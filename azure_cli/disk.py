# core
import os

# extensions
from azure.storage import BlobService

# project
from exceptions import *
from logger import Logger

class Disk:
    def __init__(self, storage_account, container):
        self.account_name = storage_account.get_name()
        self.account_key  = storage_account.get_key()
        self.container    = container
        self.upload_status = {'current_bytes': 0, 'total_bytes': 0}

    def upload(self, image, max_data_size=None, max_chunk_size=None):
        if not os.path.exists(image):
            raise AzureDiskImageNotFound("Image file %s not found" % image)
        blob_service = BlobService(self.account_name, self.account_key)
        blob_name = os.path.basename(image)

        content_encoding = None
        content_language = None
        content_md5 = None
        cache_control = None
        x_ms_blob_content_type = None
        x_ms_blob_content_encoding = None
        x_ms_blob_content_language = None
        x_ms_blob_content_md5 = None
        x_ms_blob_cache_control = None
        x_ms_meta_name_values = None
        x_ms_lease_id = None
        progress_callback = self.__upload_status

        if max_data_size:
            blob_service._BLOB_MAX_DATA_SIZE = int(max_data_size)
        if max_chunk_size:
            blob_service._BLOB_MAX_CHUNK_DATA_SIZE = int(max_chunk_size)

        # For testing progress info we set data and chunks to smaller values
        # this can also be done by global command line parameters
        #
        #blob_service._BLOB_MAX_DATA_SIZE = 1 * 1024 * 1024
        #blob_service._BLOB_MAX_CHUNK_DATA_SIZE = 4 * 1024

        try:
            blob_service.put_block_blob_from_path(
                self.container, blob_name, image,
                content_encoding, content_language, content_md5,
                cache_control,
                x_ms_blob_content_type,
                x_ms_blob_content_encoding,
                x_ms_blob_content_language,
                x_ms_blob_content_md5,
                x_ms_blob_cache_control,
                x_ms_meta_name_values,
                x_ms_lease_id,
                progress_callback
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
