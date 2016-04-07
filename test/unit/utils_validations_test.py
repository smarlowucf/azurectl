import sys
import mock
from mock import patch


from test_helper import *

import azurectl
from azurectl.utils.validations import Validations
from azurectl.azurectl_exceptions import *


class TestValidations:
    def setup(self):
        pass

    def test_good_min_length(self):
        result = Validations.validate_min_length('foo', '1234567890', 10)
        assert result is True

    @raises(AzureInvalidCommand)
    def test_bad_min_length(self):
        Validations.validate_min_length('foo', '12345', 10)

    def test_good_max_length(self):
        result = Validations.validate_max_length('foo', '1234567890', 10)
        assert result is True

    @raises(AzureInvalidCommand)
    def test_bad_max_length(self):
        Validations.validate_max_length('foo', '1234567890', 5)
