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

    def test_set_attribute(self):
        class X:
            def __init__(self):
                self.name = 'value'
        instance = X()
        Defaults.set_attribute(instance, 'name', 'foo')
        assert instance.name == 'foo'

    def test_get_attribute(self):
        class X:
            def __init__(self):
                self.name = 'value'
        instance = X()
        Defaults.get_attribute(instance, 'name')
        assert instance.name == 'value'
