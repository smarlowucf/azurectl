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
from OpenSSL.crypto import (
    dump_privatekey,
    dump_certificate,
    load_pkcs12,
    FILETYPE_PEM
)
from tempfile import NamedTemporaryFile
from urlparse import urlparse
from azure.servicemanagement import ServiceManagementService
import base64

# project
from azurectl_exceptions import (
    AzureConfigVariableNotFound,
    AzureServiceManagementError,
    AzureSubscriptionPrivateKeyDecodeError,
    AzureSubscriptionCertificateDecodeError,
    AzureSubscriptionIdNotFound,
    AzureSubscriptionParseError,
    AzureManagementCertificateNotFound,
    AzureServiceManagementUrlNotFound,
    AzureSubscriptionPKCS12DecodeError,
    AzureUnrecognizedManagementUrl
)
from constants import BLOB_SERVICE_HOST_BASE


class AzureAccount(object):
    """
        Azure Service and Storage account handling
    """
    def __init__(self, config):
        self.config = config
        self.service = None

    def storage_name(self):
        return self.config.get_storage_account_name()

    def storage_container(self):
        return self.config.get_storage_container_name()

    def subscription_id(self):
        try:
            return self.config.get_subscription_id()
        except AzureConfigVariableNotFound:
            return self.__get_first_subscription_id()

    def get_management_url(self):
        subscription = self.__get_subscription(self.subscription_id())
        try:
            url = subscription.attributes['ServiceManagementUrl'].value
        except Exception:
            raise AzureServiceManagementUrlNotFound(
                'No PublishProfile.ServiceManagementUrl found in %s' %
                self.settings
            )
        return urlparse(url).hostname

    def get_blob_service_host_base(self):
        management_url = self.get_management_url()
        try:
            return BLOB_SERVICE_HOST_BASE[management_url]
        except KeyError:
            raise AzureUnrecognizedManagementUrl(
                'No storage service host base for the management url %s' %
                management_url
            )

    def storage_key(self, name=None):
        self.__build_service_instance()
        if not name:
            name = self.storage_name()
        try:
            account_keys = self.service.get_storage_account_keys(name)
        except Exception as e:
            raise AzureServiceManagementError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return account_keys.storage_service_keys.primary

    def instance_types(self):
        self.__build_service_instance()
        result = []
        for rolesize in self.service.list_role_sizes():
            memory = rolesize.memory_in_mb
            cores = rolesize.cores
            disks = rolesize.max_data_disk_count
            size = rolesize.virtual_machine_resource_disk_size_in_mb
            instance_type = {
                rolesize.name: {
                    'memory': format(memory) + 'MB',
                    'cores': cores,
                    'max_disk_count': disks,
                    'disk_size': format(size) + 'MB'
                }
            }
            result.append(instance_type)
        return result

    def storage_names(self):
        self.__build_service_instance()
        result = []
        for storage in self.service.list_storage_accounts():
            result.append(storage.service_name)
        return result

    def publishsettings(self):
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id', 'management_url']
        )
        result = credentials(
            private_key=self.__get_private_key(),
            certificate=self.__get_certificate(),
            subscription_id=self.subscription_id(),
            management_url=self.get_management_url()
        )
        return result

    def get_service(self):
        self.__build_service_instance()
        return self.service

    def __build_service_instance(self):
        if self.service:
            return
        publishsettings = self.publishsettings()
        self.cert_file = NamedTemporaryFile()
        self.cert_file.write(publishsettings.private_key)
        self.cert_file.write(publishsettings.certificate)
        self.cert_file.flush()
        try:
            self.service = ServiceManagementService(
                publishsettings.subscription_id,
                self.cert_file.name,
                publishsettings.management_url
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
            raise AzureSubscriptionPrivateKeyDecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_certificate(self):
        p12 = self.__read_p12()
        try:
            return dump_certificate(
                FILETYPE_PEM, p12.get_certificate()
            )
        except Exception as e:
            raise AzureSubscriptionCertificateDecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_first_subscription_id(self):
        xml = self.__read_xml()
        subscriptions = xml.getElementsByTagName('Subscription')
        try:
            return subscriptions[0].attributes['Id'].value
        except Exception:
            raise AzureSubscriptionIdNotFound(
                'No Subscription.Id found in %s' % self.settings
            )

    def __get_subscription(self, subscription_id):
        xml = self.__read_xml()
        subscriptions = xml.getElementsByTagName('Subscription')
        for subscription in subscriptions:
            try:
                if subscription.attributes['Id'].value == subscription_id:
                    return subscription
            except Exception:
                raise AzureSubscriptionIdNotFound(
                    'No Subscription.Id found in %s' % self.settings
                )
        raise AzureSubscriptionIdNotFound(
            "Subscription_id '%s' not found in %s" % (
                subscription_id, self.settings
            )
        )

    def __read_xml(self):
        try:
            self.settings = self.config.get_publishsettings_file_name()
            return minidom.parse(self.settings)
        except Exception as e:
            raise AzureSubscriptionParseError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __read_p12(self):
        subscription = self.__get_subscription(self.subscription_id())
        try:
            cert = subscription.attributes['ManagementCertificate'].value
        except Exception:
            raise AzureManagementCertificateNotFound(
                'No PublishProfile.ManagementCertificate found in %s' %
                self.settings
            )
        try:
            return load_pkcs12(base64.b64decode(cert), '')
        except Exception as e:
            raise AzureSubscriptionPKCS12DecodeError(
                '%s: %s' % (type(e).__name__, format(e))
            )
