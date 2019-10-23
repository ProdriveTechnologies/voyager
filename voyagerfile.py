import json
import os
import click
from sys import exit # For generated executables

from Singleton import SingletonType

class VoyagerFile():
    def __init__(self, fileName):
        self.fileName = fileName

    def parse(self):
        with open(self.fileName) as json_file:
            self.data = json.load(json_file)

        self.version = self.data['version']
        self.libraries = self.data['libraries']
        self.type = self.data['type']
        self.solution = True
        self.projects = []

        if self.version != 1:
            raise ValueError('The version of the voyager JSON file must be 1')

        if self.libraries == None:
            raise ValueError('The libraries object is missing in the voyager JSON file')

        if self.type == 'solution':
            self.solution = True
            self.projects = self.data['projects']
        elif self.type == 'project':
            self.solution = False
        else:
            raise ValueError('Incorrect value of the type field in voyager JSON file. Supported: solution, project')
    
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
