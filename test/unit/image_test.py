import sys
import mock
from mock import patch
from nose.tools import *
from azure_cli.azure_account import AzureAccount
from azure_cli.exceptions import *
from azure_cli.image import Image

import azure_cli

from collections import namedtuple

class TestImage:
    def setup(self):
        MyStruct = namedtuple('MyStruct',
            'name label os category description location \
             affinity_group media_link'
        )
        self.list_os_images = [MyStruct(
            name           = 'some-name',
            label          = 'bob',
            os             = 'linux',
            category       = 'cloud',
            description    = 'nice',
            location       = 'here',
            affinity_group = 'ok',
            media_link     = 'url'
        )]
        account = AzureAccount('default', '../data/config')
        account.publishsettings = mock.Mock(
            return_value={
                'private_key': 'abc',
                'certificate': 'abc',
                'subscription_id': 'abc'
            }
        )
        self.image = Image(account)

    @patch('azure_cli.image.ServiceManagementService.list_os_images')
    def test_list(self, mock_list_os_images):
        mock_list_os_images.return_value = self.list_os_images
        assert self.image.list() == [{
            'name': 'some-name',
            'label': 'bob',
            'os': 'linux',
            'category': 'cloud',
            'description': 'nice',
            'location': 'here',
            'affinity_group': 'ok',
            'media_link': 'url'
        }]
