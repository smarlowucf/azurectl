import sys
from mock import patch
from nose.tools import *

import nose_helper

from azurectl.data_output import DataOutput
from azurectl.data_collector import DataCollector
import json


class TestDataOutput:
    def setup(self):
        collector = DataCollector()
        collector.add('some-name', 'some-data')
        self.expected_out = json.dumps(
            collector.get(), sort_keys=True, indent=2, separators=(',', ': ')
        )
        self.out = DataOutput(collector)

    @patch('sys.stdout')
    def test_display(self, mock_stdout):
        self.out.display()
        mock_stdout.write.assert_any_call(self.expected_out)
