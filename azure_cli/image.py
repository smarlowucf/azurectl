"""
usage: azure-cli image list

commands:
    list     list available os images for account subscription
"""

from exceptions import *
from logger import Logger

from azure.servicemanagement import ServiceManagementService

class Image:
    def __init__(self, account):
        self.subscription_id = account.get_account_subscription_id()
        self.cert_file = account.get_account_subscription_cert()

    def list(self):
        result = []
        service = ServiceManagementService(
            self.subscription_id, self.cert_file
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
