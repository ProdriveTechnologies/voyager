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
from .Singleton import SingletonType

LOCK_FILE_PATH = ".voyager/voyager.lock"

class LockFileWriter(metaclass=SingletonType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.libs = []
        self.transitive_deps = []
    
    def add_library(self, lib):
        self.libs.append(lib)

    def add_transitive_dependency(self, lib):
        self.transitive_deps.append(lib)

    def print(self):
        print(self.libs)

    def save(self):
        with open(LOCK_FILE_PATH, 'w') as outfile:
            data = {
                "libraries": self.libs,
                "transitive_dependencies": self.transitive_deps,
            }
            json.dump(data, outfile, indent=2)

class LockFileReader():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self):
        with open(LOCK_FILE_PATH) as json_file:
            self.data = json.load(json_file)
    
    def print(self):
        print("Compile dependencies:")
        for dep in self.compile_dependencies:
            print(f"  {dep['library']} @ {dep['version']}")
        print("Runtime dependencies:")
        for dep in self.runtime_dependencies:
            print(f"  {dep['library']} @ {dep['version']}")
        print("All dependencies:")
        for dep in self.all_dependencies:
            print(f"  {dep['library']} @ {dep['version']}")

    @property
    def compile_dependencies(self):
        deps = []
        for dep in self.data['libraries']:
            if 'dependency_type' in dep:
                if dep['dependency_type'] == 'compile':
                    deps.append(dep)
        return deps

    @property
    def runtime_dependencies(self):
        deps = []
        for dep in self.data['libraries']:
            if 'dependency_type' in dep:
                if dep['dependency_type'] == 'runtime':
                    deps.append(dep)
        return deps

    @property
    def all_dependencies(self):
        return self.data['libraries'] + self.data['transitive_dependencies']
