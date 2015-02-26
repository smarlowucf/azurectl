# core
from tempfile import NamedTemporaryFile

# extensions
from azure.servicemanagement import ServiceManagementService

# project
from account import Account
from service_account import ServiceAccount
from exceptions import *

class StorageAccount(Account):
    def get_name(self):
        return self.read('storage_account_name')

    def list(self):
        try:
            return self.__query_service_account_for('storage_names')
        except Exception as e:
            raise AzureStorageListError('%s (%s)' %(type(e), str(e)))

    def get_key(self, name = None):
        try:
            storage_service = self.__query_service_account_for(
                'storage_key', name
            )
            return storage_service.storage_service_keys.primary
        except Exception as e:
            raise AzureStorageKeyError('%s (%s)' %(type(e), str(e)))

    def __query_service_account_for(self, topic, name = None):
        if not name:
            name = self.get_name()
        service_account = ServiceAccount(self.account_name, self.config_file)
        cert_file = NamedTemporaryFile()
        cert_file.write(service_account.get_private_key())
        cert_file.write(service_account.get_cert())
        cert_file.flush()
        service = ServiceManagementService(
            service_account.get_subscription_id(),
            cert_file.name
        )
        if topic == 'storage_names':
            result = []
            for storage in service.list_storage_accounts():
                result.append(storage.service_name)
            return result
        elif topic == 'storage_key':
            return service.get_storage_account_keys(name)
        else:
            raise AzureInternalError(
                'StorageAccount::__query_service_account_for(invalid topic)'
            )
