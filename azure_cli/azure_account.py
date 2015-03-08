# core
from collections import namedtuple

# extensions
from xml.dom import minidom
from OpenSSL.crypto import *
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService

# project
from exceptions import *
from account import Account

class AzureAccount:
    def __init__(self, account_name=None, filename=None):
        self.config = Account(account_name, filename)

    def storage_name(self):
        return self.config.read('storage_account_name')

    def storage_key(self, name = None):
        return self.__query_account_for('storage_key', name)

    def storage_names(self):
        return self.__query_account_for('storage_names')

    def publishsettings(self):
        credentials = namedtuple('credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        p12 = self.__read_p12()
        result = credentials(
            private_key = self.__get_private_key(),
            certificate = self.__get_certificate(),
            subscription_id = self.__get_subscription_id()
        )
        return result

    def __query_account_for(self, topic, name=None):
        publishsettings = self.publishsettings()
        cert_file = NamedTemporaryFile()
        cert_file.write(publishsettings.private_key)
        cert_file.write(publishsettings.certificate)
        cert_file.flush()
        try:
            service = ServiceManagementService(
                publishsettings.subscription_id,
                cert_file.name
            )
        except Exception as e:
            raise AzureServiceManagementError('%s (%s)' %(type(e), str(e)))

        if topic == 'storage_names':
            result = []
            for storage in service.list_storage_accounts():
                result.append(storage.service_name)
            return result
        elif topic == 'storage_key':
            if not name:
                name = self.storage_name()
            return service.get_storage_account_keys(
                name
            ).storage_service_keys.primary
        else:
            raise AzureInternalError(
                'AzureAccount::__query_account_for(invalid topic)'
            )

    def __get_private_key(self):
        p12 = self.__read_p12()
        return dump_privatekey(
            FILETYPE_PEM, p12.get_privatekey()
        )

    def __get_certificate(self):
        p12 = self.__read_p12()
        return dump_certificate(
            FILETYPE_PEM, p12.get_certificate()
        )

    def __get_subscription_id(self):
        xml = self.__read_xml()
        subscriptions = xml.getElementsByTagName('Subscription')
        try:
            return subscriptions[0].attributes['Id'].value
        except:
            raise AzureSubscriptionIdNotFound(
                "No Subscription.Id found in %s" % self.settings
            )

    def __read_xml(self):
        self.settings = self.config.read('publishsettings')
        return minidom.parse(self.settings)

    def __read_p12(self):
        xml = self.__read_xml()
        profile = xml.getElementsByTagName('Subscription')
        try:
            cert = profile[0].attributes['ManagementCertificate'].value
        except:
            raise AzureManagementCertificateNotFound(
                "No PublishProfile.ManagementCertificate found in %s" % \
                self.settings
            )
        return load_pkcs12(cert.decode("base64"), '')
