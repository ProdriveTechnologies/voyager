# Copyright 2021 Prodrive Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import click
from sys import exit  # For generated executables
from typing import Optional
from pathlib import Path
import semver


class VoyagerFile():
    def __init__(self, fileName):
        self.fileName = fileName

    def parse(self):
        with open(self.fileName) as json_file:
            try:
                self.data = json.load(json_file)
            except json.JSONDecodeError as e:
                raise ValueError(F"Could not parse {self.fileName}: {e}")

        self.version = self.data.get('version', None)
        self.libraries = self.data.get('libraries', None)
        self.type = self.data.get('type', None)
        self.solution = True
        self.projects = []
        self.generators = self.data.get('generators', ['msbuild'])
        self.build_tools = self.data.get('build_tools', [])

        if self.version != 1:
            raise ValueError(f'The version element in {self.fileName} is missing or not set to 1')

        if self.libraries == None:
            raise ValueError(f'The libraries element is missing in {self.fileName}')

        if self.type == 'solution':
            self.solution = True
            self.projects = self.data['projects']
        elif self.type == 'project':
            self.solution = False
        elif self.type == 'overlay':
            self.solution = 'false'
        else:
            raise ValueError(f'The type element in {self.fileName} is missing or not set to: solution, project, overlay')

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
                    over['overlay'] = True
                    library.update(over)
                    break

    def add_library(self, library_string: str, force_version: bool, directory: Optional[str]):
        """
        Add a library to the voyager.json and save the file.
        The library_string must use the following format: example-generic-local/Utils/Exceptions/1.2.0
        """
        split = library_string.split('/')
        repo = split[0]
        version = split[-1]
        package = library_string.replace(f"{repo}/", '').replace(f"/{version}", '')

        # filter out the patch number
        if semver.valid_range(version, True):
            vers = semver.parse(version, True)
            version = f"{vers.major}.{vers.minor}"

        elem = {
            "repo": repo,
            "library": package,
            "version": version
        }

        if force_version:
            elem['force_version'] = True

        self.data['libraries'].append(elem)

        print("Adding Library:")
        print(f"  Repo:    {repo}")
        print(f"  Library: {package}")
        if force_version:
            print(f"  Version: {version} (Force Version)")
        else:
            print(f"  Version: {version}")

        file_path = Path("voyager.json")

        if directory is not None:
            file_path = directory / file_path

        with open(file_path, 'w') as outfile:
            json.dump(self.data, outfile, indent=2)

    @staticmethod
    def generate_empty_file():
        data = {}
        data['version'] = 1
        data['type'] = "TODO: solution or project"
        data['libraries'] = []

        if not os.path.isfile('voyager.json'):
            click.echo("Generating empty voyager.json")
            with open('voyager.json', 'w') as outfile:
                json.dump(data, outfile, indent=2)
        else:
            click.echo(click.style(u'File already exists', fg='red'))
            exit(1)
