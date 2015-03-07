# core
from tempfile import NamedTemporaryFile

# extensions
from azure.servicemanagement import ServiceManagementService

# project
from exceptions import *
from logger import Logger

class Image:
    def __init__(self, account):
        self.account = account

    def list(self):
        result = []
        cert_file = NamedTemporaryFile()
        publishsettings = self.account.publishsettings()
        cert_file.write(publishsettings['private_key'])
        cert_file.write(publishsettings['certificate'])
        cert_file.flush()
        service = ServiceManagementService(
            publishsettings['subscription_id'],
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
            raise AzureOsImageListError('%s (%s)' %(type(e), str(e)))
        return result
