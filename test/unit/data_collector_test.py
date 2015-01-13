import sys
from nose.tools import *
from azure_cli.data_collector import DataCollector

class TestDataCollector:
    def setup(self):
        self.collector = DataCollector()
        self.collector.add('some-name', 'some-data')

    def test_get(self):
        assert self.collector.get() == {'some-name': 'some-data'}
