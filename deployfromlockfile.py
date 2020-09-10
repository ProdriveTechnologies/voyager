from lockfile import LockFileReader
from buildinfo import Package

def deploy_all_dependencies():
    reader = LockFileReader()
    reader.parse()
    reader.print()

    for dep in reader.all_dependecies:
        print(dep)
        pack = Package(dep['library'], dep['version'], dep['package_path'], dep.get('options', []), False, False)
        print(f"  {pack.bin_paths}")
