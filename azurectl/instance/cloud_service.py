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
import base64
import subprocess
from dns.resolver import Resolver
from tempfile import NamedTemporaryFile

# project
from ..azurectl_exceptions import (
    AzureCloudServiceAddressError,
    AzureCloudServiceOpenSSLError,
    AzureCloudServiceAddCertificateError,
    AzureCloudServiceCreateError,
    AzureCloudServiceDeleteError
)
from ..management.request_result import RequestResult
from ..defaults import Defaults


class CloudService(object):
    """
        Implements creation/deletion and management of cloud
        services required to run virtual machine instances
    """
    def __init__(self, account):
        self.account = account
        self.service = self.account.get_management_service()

    def get_pem_certificate(self, ssh_private_key_file):
        """
            create PEM certificate from given ssh private key file
        """
        openssl = subprocess.Popen(
            [
                'openssl', 'req', '-x509',
                '-key', ssh_private_key_file,
                '-days', '365',
                '-subj', '/C=US/ST=Denial/L=Denial/O=Dis/CN=www.azure.com',
                '-newkey', 'rsa:2048'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        pem_cert, openssl_error = openssl.communicate()
        if openssl.returncode != 0:
            raise AzureCloudServiceOpenSSLError(
                '%s' % openssl_error
            )
        return pem_cert

    def get_fingerprint(self, pem_cert):
        """
            create sha1 fingerprint from given pem base64 certificate
        """
        pem_cert_file = NamedTemporaryFile()
        pem_cert_file.write(pem_cert)
        pem_cert_file.flush()
        openssl = subprocess.Popen(
            [
                'openssl', 'x509', '-noout',
                '-in', pem_cert_file.name,
                '-fingerprint', '-sha1'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        fingerprint, openssl_error = openssl.communicate()
        if openssl.returncode != 0:
            raise AzureCloudServiceOpenSSLError(
                '%s' % openssl_error
            )
        fingerprint = fingerprint.split('=')[1]
        fingerprint = fingerprint.replace(':', '')
        return fingerprint.strip()

    def add_certificate(
        self, cloud_service_name, ssh_private_key_file
    ):
        """
            create Azure conform certificate from given ssh private
            key and add the CER formatted public pem file to the
            cloud service. The method returns the certificate
            fingerprint
        """
        pem_cert = self.get_pem_certificate(
            ssh_private_key_file
        )
        pem_cert_file = NamedTemporaryFile()
        pem_cert_file.write(pem_cert)
        pem_cert_file.flush()
        openssl = subprocess.Popen(
            [
                'openssl', 'pkcs12', '-export',
                '-inkey', ssh_private_key_file,
                '-in', pem_cert_file.name,
                '-passout', 'pass:'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        pfx_cert, openssl_error = openssl.communicate()
        if openssl.returncode != 0:
            raise AzureCloudServiceOpenSSLError(
                '%s' % openssl_error
            )
        try:
            add_cert_request = self.service.add_service_certificate(
                cloud_service_name, base64.b64encode(pfx_cert), 'pfx', u''
            )
        except Exception as e:
            raise AzureCloudServiceAddCertificateError(
                '%s: %s' % (type(e).__name__, format(e))
            )
        # Wait for the certficate to be created
        request_result = RequestResult(add_cert_request.request_id)
        request_result.wait_for_request_completion(
            self.service
        )
        return self.get_fingerprint(pem_cert)

    def create(
        self, cloud_service_name, location,
        description='CloudService', label=None
    ):
        """
            create cloud service with specified name and return the
            request id
        """
        service_record = {
            'service_name': cloud_service_name,
            'label': cloud_service_name,
            'description': description,
            'location': location
        }
        if label:
            service_record['label'] = label

        if self.__get_cloud_service_properties(cloud_service_name):
            # indicate existing cloud service with request id: 0
            return 0

        if self.__cloud_service_url_in_use(cloud_service_name, location):
            message = [
                'The cloud service name "%s"',
                'is already in use in another region',
                'please choose a different name.'
            ]
            raise AzureCloudServiceAddressError(
                ' '.join(message) % cloud_service_name
            )

        try:
            result = self.service.create_hosted_service(**service_record)
            return (result.request_id)
        except Exception as e:
            raise AzureCloudServiceCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def delete(self, cloud_service_name, complete=False):
        """
            delete specified cloud service, if complete is set to true
            all OS/data disks and the source blobs for the disks will be
            deleted too
        """
        try:
            result = self.service.delete_hosted_service(
                cloud_service_name, complete
            )
            return (result.request_id)
        except Exception as e:
            raise AzureCloudServiceDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __get_cloud_service_properties(self, cloud_service_name):
        try:
            return self.service.get_hosted_service_properties(
                cloud_service_name
            )
        except Exception:
            pass

    def __cloud_service_url_in_use(self, cloud_service_name, location):
        dns_resolver = Resolver()
        cloud_service_url = \
            cloud_service_name + '.' + Defaults.get_azure_domain(location)
        try:
            return dns_resolver.query(cloud_service_url, 'A')
        except Exception:
            pass
