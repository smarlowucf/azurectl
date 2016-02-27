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
from azurectl_exceptions import *
from defaults import Defaults


class AsmObject(object):

    def __init__(self, account):
        self.setup_account(account)
        self.service = self.get_service()

    def setup_account(self, account):
        self.account = account
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.cert_file = NamedTemporaryFile()
        self.publishsettings = self.account.publishsettings()
        self.cert_file.write(self.publishsettings.private_key)
        self.cert_file.write(self.publishsettings.certificate)
        self.cert_file.flush()

    def get_service(self):
        return ServiceManagementService(
            self.publishsettings.subscription_id,
            self.cert_file.name,
            self.publishsettings.management_url
        )
