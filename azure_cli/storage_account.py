from account import Account
from service_account import ServiceAccount
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService
from exceptions import *

class StorageAccount(Account):
    def get_account_name(self):
        return self.read('storage_account_name')

    def get_account_key(self):
        try:
            storage_service = self.__query_service_account_for('storage_key')
            return storage_service.storage_service_keys.primary
        except Exception as e:
            raise AzureStorageKeyError('%s (%s)' %(type(e), str(e)))

    def __query_service_account_for(self, topic):
        service_account = ServiceAccount(self.account_name, self.config_file)
        cert_file = NamedTemporaryFile()
        cert_file.write(service_account.get_private_key())
        cert_file.write(service_account.get_cert())
        cert_file.flush()
        service = ServiceManagementService(
            service_account.get_subscription_id(),
            cert_file.name
        )
        if topic == 'storage_accounts':
            return service.list_storage_accounts()
        elif topic == 'storage_key':
            return service.get_storage_account_keys(self.get_account_name())
        else:
            raise AzureInternalError(
                'StorageAccount::__query_service_account_for(invalid topic)'
            )
