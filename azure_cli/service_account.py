from exceptions import *

from account import Account
from xml.dom import minidom
from OpenSSL.crypto import *

class ServiceAccount(Account):
    def get_private_key(self):
        p12 = self.__read_p12()
        return dump_privatekey(
            FILETYPE_PEM, p12.get_privatekey()
        )

    def get_cert(self):
        p12 = self.__read_p12()
        return dump_certificate(
            FILETYPE_PEM, p12.get_certificate()
        )

    def get_subscription_id(self):
        xml = self.__read_xml()
        subscriptions = xml.getElementsByTagName('Subscription')
        try:
            return subscriptions[0].attributes['Id'].value
        except:
            raise AzureSubscriptionIdNotFound(
                "No Subscription.Id found in %s" % self.settings
            )

    def __read_xml(self):
        self.settings = self.read('publishsettings')
        return minidom.parse(self.settings)

    def __read_p12(self):
        xml = self.__read_xml()
        profile = xml.getElementsByTagName('PublishProfile')
        try:
            cert = profile[0].attributes['ManagementCertificate'].value
        except:
            raise AzureManagementCertificateNotFound(
                "No PublishProfile.ManagementCertificate found in %s" % \
                self.settings
            )
        return load_pkcs12(cert.decode("base64"), '')
