import json
from Singleton import SingletonType

LOCK_FILE_PATH = "libs/voyager.lock"

class LockFileWriter(metaclass=SingletonType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.libs = []
    
    def add_dependency(self, lib):
        self.libs.append(lib)

    def print(self):
        print(self.libs)

    def save(self):
        with open(LOCK_FILE_PATH, 'w') as outfile:
            json.dump(self.libs, outfile, indent=2)

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

    @property
    def compile_dependencies(self):
        deps = []
        for dep in self.data:
            if 'dependency_type' in dep:
                if dep['dependency_type'] == 'compile':
                    deps.append(dep)
        return deps

    @property
    def runtime_dependencies(self):
        deps = []
        for dep in self.data:
            if 'dependency_type' in dep:
                if dep['dependency_type'] == 'runtime':
                    deps.append(dep)
        return deps