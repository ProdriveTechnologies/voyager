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
from pathlib import Path

import semver

class VoyagerPackageFile():
    def __init__(self, template_filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._template_filename = template_filename
        self._dependencies = []
        self._template_contents = None

    def parse_template(self):
        with open(self._template_filename) as json_file:
            self._template_contents = json.load(json_file)

    def add_dependencies(self, deps):
        for d in deps:
            v = semver.parse(d['version'], False)
            if v:
                # Pin to the major and minor version
                d['version'] = f"{v.major}.{v.minor}"
            else:
                print(f"WARNING: The dependency {d['library']} has a non valid version '{d['version']}' for release")
            # Rename dependency_type to type for package file
            d['type'] = d['dependency_type']
            del d['dependency_type']

            fields_to_remove = ['force_version', 'output_dir', 'overlay', 'package_path']
            for f in fields_to_remove:
                if f in d:
                    if f != 'package_path':  # Do not show message for package path since it is not a user parameter
                        print(f"{f} found for {d['library']}, this will be removed in package file")
                    del d[f]

            self._dependencies.append(d)

    def save(self):
        if not self._template_contents:
            raise ValueError('The parse function must run before save can be called')

        self._template_contents['dependencies'] += self._dependencies

        p = Path(self._template_filename)
        f = p.parent / 'voyager_package.json'
        with open(f, 'w') as outfile:
            json.dump(self._template_contents, outfile, indent=2)
