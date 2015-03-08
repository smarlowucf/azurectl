# core
import json

class DataCollector:
    data = {}

    def __init__(self):
        self.data = {}

    def add(self, name, data):
        self.data[name] = data

    def get(self):
        return self.data

    def json(self):
        return json.dumps(
            self.data, sort_keys=True, indent=4, separators=(',', ': ')
        )
