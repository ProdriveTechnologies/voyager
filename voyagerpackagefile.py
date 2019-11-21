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
            print(d['version'])
            v = semver.clean(d['version'], False)
            if v:
                # Pin to the major and minor version
                d['version'] = f"{v.major}.{v.minor}"
            else:
                print(f"WARNING: The dependency {d['library']} has a non valid version '{d['version']}' for release")
            # Rename dependency_type to type for package file
            d['type'] = d['dependency_type']
            del d['dependency_type']
            self._dependencies.append(d)

    def save(self):
        if not self._template_contents:
            raise ValueError('The parse function must run before save can be called')

        self._template_contents['dependencies'] += self._dependencies

        p = Path(self._template_filename)
        f = p.parent / 'voyager_package.json'
        with open(f, 'w') as outfile:
            json.dump(self._template_contents, outfile, indent=2)
    