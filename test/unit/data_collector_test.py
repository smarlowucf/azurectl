import sys
from nose.tools import *

import nose_helper

from azurectl.data_collector import DataCollector


class TestDataCollector:
    def setup(self):
        self.collector = DataCollector()

    def test_get(self):
        assert self.collector.get() == {}

    def test_add(self):
        self.collector.add('some-name', 'some-data')
        assert self.collector.get() == {'some-name': 'some-data'}
