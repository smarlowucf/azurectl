"""
usage: azure-cli image list

commands:
    list     list available os images for account subscription
"""

from exceptions import *
from logger import Logger

from azure.servicemanagement import ServiceManagementService
from tempfile import NamedTemporaryFile

class Image:
    def __init__(self, account):
        self.account = account

    def list(self):
        result = []
        cert_file = NamedTemporaryFile()
        cert_file.write(self.account.get_private_key())
        cert_file.write(self.account.get_cert())
        cert_file.flush()
        service = ServiceManagementService(
            self.account.get_subscription_id(),
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
