class DataCollector:
    data = {}

    def __init__(self):
        self.data = {}

    def add(self, name, data):
        self.data[name] = data

    def get(self):
        return self.data
