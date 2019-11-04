import json

import semver

class VoyagerPackageFile():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dependencies = []
        self._template_contents = None

    def parse_template(self):
        with open('voyager_package.json.template') as json_file:
            self._template_contents = json.load(json_file)

    def add_dependencies(self, deps):
        for d in deps:
            v = semver.valid(d['version'], False)
            if v:
                d['version'] = f"{v.major}.{v.minor}"
            else:
                raise ValueError(f"The dependency {d['library']} has a non valid version {d['version']} for release")
            versionarr = d['version']
            self._dependencies.append(d)

    def save(self):
        if not self._template_contents:
            raise ValueError('The parse function must run before save can be called')

        self._template_contents['dependencies'] += self._dependencies

        with open('voyager_package.json', 'w') as outfile:
            json.dump(self._template_contents, outfile, indent=2)
    