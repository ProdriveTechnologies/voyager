import json

from Singleton import SingletonType

class VoyagerFile(metaclass=SingletonType):
    def __init__(self, fileName):
        self.fileName = fileName

    def parse(self):
        with open(self.fileName) as json_file:
            self.data = json.load(json_file)

        self.version = self.data['version']
        self.libraries = self.data['libraries']
    
    def print(self):
        print(self.data)