import json
import os
import click
from sys import exit # For generated executables

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

    @staticmethod
    def generate_empty_file():
        data = {}
        data['version'] = 1
        data['libraries'] = [{
            "repo": "",
            "library": "",
            "version": ""
        }]

        if not os.path.isfile('voyager.json'):
            click.echo("Generating empty config file")
            with open('voyager.json', 'w') as outfile:
                json.dump(data, outfile, indent=2)
        else:
            click.echo(click.style(u'File already exists', fg='red'))
            exit(1)
