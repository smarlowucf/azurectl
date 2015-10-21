import sys
import mock
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.azure_account import AzureAccount
from azurectl.config import Config
from azurectl.azurectl_exceptions import *
from azurectl.cloud_service import CloudService

import azurectl

from collections import namedtuple


class TestCloudService:
    def setup(self):
        MyResult = namedtuple(
            'MyResult',
            'request_id'
        )
        self.myrequest = MyResult(request_id=42)
        MyStruct = namedtuple(
            'MyStruct',
            'name label os category description location \
             affinity_group media_link'
        )
        self.list_os_images = [MyStruct(
            name='some-name',
            label='bob',
            os='linux',
            category='cloud',
            description='nice',
            location='here',
            affinity_group='ok',
            media_link='url'
        )]
        account = AzureAccount(
            Config(
                region_name='East US 2', filename='../data/config'
            )
        )
        credentials = namedtuple(
            'credentials',
            ['private_key', 'certificate', 'subscription_id']
        )
        account.publishsettings = mock.Mock(
            return_value=credentials(
                private_key='abc',
                certificate='abc',
                subscription_id='4711'
            )
        )
        account.storage_key = mock.Mock()
        self.service = CloudService(account)

    @patch('azurectl.cloud_service.CloudService.get_pem_certificate')
    @patch('azurectl.cloud_service.CloudService.get_fingerprint')
    @patch('azurectl.cloud_service.ServiceManagementService.add_service_certificate')
    @patch('azurectl.cloud_service.RequestResult')
    @patch('subprocess.Popen')
    @patch('base64.b64encode')
    def test_add_certificate(
        self, mock_base64, mock_popen, mock_request_result, mock_add_cert,
        mock_fingerprint, mock_getpem
    ):
        mock_openssl = mock.Mock()
        mock_openssl.communicate = mock.Mock(
            return_value=['pfx-data-stream', 'error']
        )
        mock_openssl.returncode = 0
        mock_popen.return_value = mock_openssl
        mock_getpem.return_value = 'pem-base64-stream'
        mock_base64.return_value = 'base64-pfx-stream'
        mock_fingerprint.return_value = 'finger-print'
        assert self.service.add_certificate(
            'cloud-service', 'ssh-private-key'
        ) == 'finger-print'
        mock_getpem.assert_called_once_with('ssh-private-key')
        mock_popen.assert_called_once_with(
            [
                'openssl', 'pkcs12', '-export',
                '-inkey', 'ssh-private-key',
                '-in', mock.ANY,
                '-passout', 'pass:'
            ],
            stderr=-1,
            stdout=-1
        )
        mock_base64.assert_called_once_with(
            'pfx-data-stream'
        )
        mock_add_cert.assert_called_once_with(
            'cloud-service', 'base64-pfx-stream', 'pfx', u''
        )
        mock_fingerprint.assert_called_once_with(
            'pem-base64-stream'
        )

    @patch('subprocess.Popen')
    def test_get_pem_certificate(self, mock_popen):
        mock_openssl = mock.Mock()
        mock_openssl.communicate = mock.Mock(
            return_value=['SHA1 Fingerprint=02:8F:82', 'error']
        )
        mock_openssl.returncode = 0
        mock_popen.return_value = mock_openssl
        self.service.get_pem_certificate('ssh-private-key')
        mock_popen.assert_called_once_with(
            [
                'openssl', 'req', '-x509', '-key', 'ssh-private-key',
                '-days', '365',
                '-subj', '/C=US/ST=Denial/L=Denial/O=Dis/CN=www.azure.com',
                '-newkey', 'rsa:2048'
            ],
            stderr=-1,
            stdout=-1
        )

    @patch('subprocess.Popen')
    def test_get_fingerprint(self, mock_popen):
        mock_openssl = mock.Mock()
        mock_openssl.communicate = mock.Mock(
            return_value=['SHA1 Fingerprint=02:8F:82', 'error']
        )
        mock_openssl.returncode = 0
        mock_popen.return_value = mock_openssl
        self.service.get_fingerprint('pem-base64-stream')
        mock_popen.assert_called_once_with(
            [
                'openssl', 'x509', '-noout', '-in', mock.ANY,
                '-fingerprint', '-sha1'
            ],
            stderr=-1,
            stdout=-1
        )

    @raises(AzureCloudServiceOpenSSLError)
    def test_get_fingerprint_raise_openssl_error(self):
        self.service.get_fingerprint('foo')

    @raises(AzureCloudServiceOpenSSLError)
    def test_get_pem_certificate_raise_openssl_error(self):
        self.service.get_pem_certificate('foo')

    @patch('azurectl.cloud_service.CloudService.get_pem_certificate')
    @patch('subprocess.Popen')
    @raises(AzureCloudServiceOpenSSLError)
    def test_add_certificate_raise_openssl_error(self, mock_popen, mock_getpem):
        mock_openssl = mock.Mock()
        mock_openssl.communicate = mock.Mock(
            return_value=['cer-data-stream', 'error']
        )
        mock_openssl.returncode = 1
        mock_popen.return_value = mock_openssl
        mock_getpem.return_value = 'pem-base64-stream'
        self.service.add_certificate(
            'cloud-service', '../data/id_test'
        )

    @patch('azurectl.cloud_service.ServiceManagementService.add_service_certificate')
    @raises(AzureCloudServiceAddCertificateError)
    def test_add_certificate_raise_add_error(self, mock_add_cert):
        mock_add_cert.side_effect = AzureCloudServiceAddCertificateError
        self.service.add_certificate('cloud-service', '../data/id_test')

    @patch('azurectl.cloud_service.ServiceManagementService.create_hosted_service')
    @patch('azurectl.cloud_service.ServiceManagementService.get_hosted_service_properties')
    @patch('dns.resolver.Resolver.query')
    def test_create(self, mock_query, mock_get_service, mock_create_service):
        mock_query.side_effect = Exception
        mock_get_service.side_effect = AzureError('does-not-exist')
        self.service.create('cloud-service', 'West US', 'my-cloud', 'label')
        mock_get_service.assert_called_once_with('cloud-service')
        mock_create_service.assert_called_once_with(
            service_name='cloud-service',
            description='my-cloud',
            location='West US',
            label='label'
        )

    @patch('azurectl.cloud_service.ServiceManagementService.create_hosted_service')
    @patch('azurectl.cloud_service.ServiceManagementService.get_hosted_service_properties')
    @patch('dns.resolver.Resolver.query')
    @raises(AzureCloudServiceAddressError)
    def test_create_cloud_service_in_use(self, mock_query, mock_get_service, mock_create_service):
        mock_query.return_value = 'some-address-result'
        mock_get_service.side_effect = AzureError('does-not-exist')
        self.service.create('cloud-service', 'West US', 'my-cloud', 'label')

    @patch('azurectl.cloud_service.ServiceManagementService.delete_hosted_service')
    def test_delete(self, mock_delete_service):
        mock_delete_service.return_value = self.myrequest
        request_id = self.service.delete('cloud-service')
        mock_delete_service.assert_called_once_with(
            'cloud-service', False
        )
        assert request_id == 42

    @patch('azurectl.cloud_service.ServiceManagementService.create_hosted_service')
    @patch('azurectl.cloud_service.ServiceManagementService.get_hosted_service_properties')
    @patch('dns.resolver.Resolver.query')
    @raises(AzureCloudServiceCreateError)
    def test_create_service_error(self, mock_query, mock_get_service, mock_create_service):
        mock_query.side_effect = Exception
        mock_get_service.side_effect = Exception
        mock_create_service.side_effect = AzureCloudServiceCreateError
        self.service.create('cloud-service', 'West US', 'my-cloud', 'label')

    @patch('azurectl.cloud_service.ServiceManagementService.create_hosted_service')
    @patch('azurectl.cloud_service.ServiceManagementService.get_hosted_service_properties')
    def test_create_service_exists(self, mock_get_service, mock_create_service):
        request_id = self.service.create(
            'cloud-service', 'region', 'my-cloud', 'label'
        )
        assert request_id == 0

    @patch('azurectl.cloud_service.ServiceManagementService.delete_hosted_service')
    @raises(AzureCloudServiceDeleteError)
    def test_delete_service_error(self, mock_delete_service):
        mock_delete_service.side_effect = AzureCloudServiceDeleteError
        self.service.delete('cloud-service')
