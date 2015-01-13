import sys
import mock
from nose.tools import *
from azure_cli.service_account import ServiceAccount
from azure_cli.exceptions import *
from azure_cli.image import Image

import azure_cli

from collections import namedtuple

class FakeServiceManagementService:
    def list_os_images(self):
        MyStruct = namedtuple('MyStruct',
            'name label os category description location \
             affinity_group media_link'
        )
        return [MyStruct(
            name           = 'some-name',
            label          = 'bob',
            os             = 'linux',
            category       = 'cloud',
            description    = 'nice',
            location       = 'here',
            affinity_group = 'ok',
            media_link     = 'url'
        )]


class TestImage:
    def setup(self):
        account = ServiceAccount('default', '../data/config')
        self.image = Image(account)

    def test_list(self):
        azure_cli.image.ServiceManagementService = mock.Mock(
            return_value=FakeServiceManagementService()
        )
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
