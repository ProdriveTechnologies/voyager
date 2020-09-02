import json
import os
import click
from sys import exit # For generated executables
import semver

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
        self.generators = self.data.get('generators', ['msbuild'])
        self.build_tools = self.data.get('build_tools', [])

        if self.version != 1:
            raise ValueError('The version of the voyager JSON file must be 1')

        if self.libraries == None:
            raise ValueError('The libraries object is missing in the voyager JSON file')

        if self.type == 'solution':
            self.solution = True
            self.projects = self.data['projects']
        elif self.type == 'project':
            self.solution = False
        elif self.type == 'overlay':
            self.solution = 'false'
        else:
            raise ValueError('Incorrect value of the type field in voyager JSON file. Supported: solution, project, overlay')

    def print(self):
        print(self.data)

    def has_build_tools(self):
        return len(self.build_tools) > 0

    def combine_with_overlay(self, overlay):
        if overlay is None:
            return

        self._combine_libraries_or_build_tools(self.libraries, overlay.libraries)
        self._combine_libraries_or_build_tools(self.build_tools, overlay.build_tools)

    def _combine_libraries_or_build_tools(self, container, container_overlay):
        # Search for each library or build_tool in the voyager.json file if there is an overlay available
        for library in container:
            repo = library['repo']
            lib = library['library']
            # version = library['version']

            for over in container_overlay:
                repo_over = over['repo']
                lib_over = over['library']
                # version_over = over['version']

                if repo == repo_over and lib == lib_over:
                    library.update(over)
                    break


    def add_library(self, library_string: str):
        """
        Add a library to the voyager.json and save the file.
        The library_string must use the following format: siatd-generic-local/Utils/Exceptions/1.2.0
        """
        split = library_string.split('/')
        repo = split[0]
        version = split[-1]
        package = library_string.replace(f"{repo}/", '').replace(f"/{version}", '')

        # filter out the patch number
        if semver.valid_range(version, True):
            vers = semver.parse(version, True)
            version = f"{vers.major}.{vers.minor}"

        self.data['libraries'].append({
            "repo": repo,
            "library": package,
            "version": version
        })

        print("Adding Library:")
        print(f"  Repo:    {repo}")
        print(f"  Library: {package}")
        print(f"  Version: {version}")

        with open('voyager.json', 'w') as outfile:
            json.dump(self.data, outfile, indent=2)

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
