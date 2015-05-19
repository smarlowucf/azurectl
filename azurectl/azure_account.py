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
from collections import namedtuple
from xml.dom import minidom
from OpenSSL.crypto import *
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService

# project
from azurectl_exceptions import *
from config import Config


class AzureAccount:
    """
        Azure Service and Storage account handling
    """
    def __init__(self, account_name=None, filename=None):
        self.config = Config(account_name, filename)

    def storage_name(self):
        return self.config.get_option('storage_account_name')

    def storage_container(self):
        return self.config.get_option('storage_container_name')

    def storage_key(self, name=None):
        return self.__query_account_for('storage_key', name)

    def storage_names(self):
        return self.__query_account_for('storage_names')

    def publishsettings(self):
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        p12 = self.__read_p12()
        result = credentials(
            private_key=self.__get_private_key(),
            certificate=self.__get_certificate(),
            subscription_id=self.__get_subscription_id()
        )
        return result

    def __query_account_for(self, information_type, name=None):
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
            if information_type == 'storage_names':
                result = []
                for storage in service.list_storage_accounts():
                    result.append(storage.service_name)
                return result
            elif information_type == 'storage_key':
                if not name:
                    name = self.storage_name()
                return service.get_storage_account_keys(
                   name
                ).storage_service_keys.primary
            raise AzureInternalError(
                'AzureAccount::__query_account_for(invalid information type)'
            )
        except Exception as e:
            raise AzureServiceManagementError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_private_key(self):
        p12 = self.__read_p12()
        try:
            return dump_privatekey(
                FILETYPE_PEM, p12.get_privatekey()
            )
        except Exception as e:
            raise AzureSubscriptionDecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_certificate(self):
        p12 = self.__read_p12()
        try:
            return dump_certificate(
                FILETYPE_PEM, p12.get_certificate()
            )
        except Exception as e:
            raise AzureSubscriptionDecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_subscription_id(self):
        xml = self.__read_xml()
        subscriptions = xml.getElementsByTagName('Subscription')
        try:
            return subscriptions[0].attributes['Id'].value
        except:
            raise AzureSubscriptionIdNotFound(
                'No Subscription.Id found in %s' % self.settings
            )

    def __read_xml(self):
        try:
            self.settings = self.config.get_option('publishsettings')
            return minidom.parse(self.settings)
        except Exception as e:
            raise AzureSubscriptionParseError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __read_p12(self):
        xml = self.__read_xml()
        try:
            profile = xml.getElementsByTagName('Subscription')
            cert = profile[0].attributes['ManagementCertificate'].value
        except:
            raise AzureManagementCertificateNotFound(
                'No PublishProfile.ManagementCertificate found in %s' %
                self.settings
            )
        try:
            return load_pkcs12(cert.decode("base64"), '')
        except Exception as e:
            raise AzureSubscriptionDecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )
