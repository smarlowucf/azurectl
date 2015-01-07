class DataCollector:
    data = {}

    def add(self, name, data):
        self.data[name] = data

    def get(self):
        return self.data
