# Copyright (c) 2016 SUSE.  All rights reserved.
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
import os
import collections
from tempfile import NamedTemporaryFile
from azure.servicemanagement import ServiceManagementService

# project
from azurectl_exceptions import (
    AzureReservedIpListError
)
from defaults import Defaults


class ReservedIp(object):
    """
        Implements Azure reserved IP address management. This includes the
        following tasks:
        + creation and deletion of IP address reservations
        + listing reserved IP addresses
    """
    def __init__(self, account):
        self.account = account
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.cert_file = NamedTemporaryFile()
        self.publishsettings = self.account.publishsettings()
        self.cert_file.write(self.publishsettings.private_key)
        self.cert_file.write(self.publishsettings.certificate)
        self.cert_file.flush()

    def list(self):
        result = []
        service = self.__get_service()
        try:
            for ip in service.list_reserved_ip_addresses():
                result.append(self.__decorate_for_results(ip))
        except Exception as e:
            raise AzureReservedIpListError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        return result

    def __get_service(self):
        return ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name,
            self.publishsettings.management_url
        )

    def __decorate_for_results(self, ip):
        return {
            'name': ip.name,
            'address': ip.address,
            'state': ip.state,
            'in_use': ip.in_use,
            'cloud_service_name': ip.service_name,
            'instance_name': ip.deployment_name,
            'region': ip.location
        }
