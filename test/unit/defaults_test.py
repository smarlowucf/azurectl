from nose.tools import *
from mock import patch

import nose_helper
import mock

from azurectl.azurectl_exceptions import *
from azurectl.defaults import Defaults


class TestDefaults:
    def test_get_azure_domain(self):
        assert Defaults.get_azure_domain('West US') == 'cloudapp.net'

    @raises(AzureDomainLookupError)
    def test_get_azure_domain_raises(self):
        Defaults.get_azure_domain('region-does-not-exist')

    def test_get_nameservers(self):
        assert Defaults.get_nameservers() == ['8.8.8.8']
