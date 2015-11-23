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
# project
from azurectl_exceptions import AzureDomainLookupError


class Defaults(object):
    """
        Default values and static information
    """
    @classmethod
    def get_azure_domain(self, region):
        """
            return domain name according to the specified Azure region
        """
        azure_domain = {
            'Australia East': 'cloudapp.net',
            'Australia Southeast': 'cloudapp.net',
            'Brazil South': 'cloudapp.net',
            'Central India': 'cloudapp.net',
            'Central US': 'cloudapp.net',
            'East Asia': 'cloudapp.net',
            'East US 2': 'cloudapp.net',
            'East US': 'cloudapp.net',
            'Japan East': 'cloudapp.net',
            'Japan West': 'cloudapp.net',
            'North Central US': 'cloudapp.net',
            'North Europe': 'cloudapp.net',
            'South Central US': 'cloudapp.net',
            'Southeast Asia': 'cloudapp.net',
            'South India': 'cloudapp.net',
            'West Europe': 'cloudapp.net',
            'West India': 'cloudapp.net',
            'West US': 'cloudapp.net'
        }
        if region not in azure_domain:
            raise AzureDomainLookupError(
                'Specified region %s not in lookup table'
            )
        return azure_domain[region]

    @classmethod
    def get_attribute(self, instance, name):
        return getattr(instance, name)

    @classmethod
    def set_attribute(self, instance, name, value):
        return setattr(instance, name, value)
