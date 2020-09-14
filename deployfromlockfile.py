from distutils.dir_util import copy_tree
import distutils.errors
from pathlib import PurePath

import click

from lockfile import LockFileReader
from buildinfo import Package


def deploy_all_dependencies(deploy_dir):
    reader = LockFileReader()
    reader.parse()

    click.echo(click.style('Dependencies with bin dirs:', fg='cyan'))
    copied = []
    for dep in reader.all_dependencies:
        pack = Package(dep['library'], dep['version'], dep['package_path'], dep.get('options', []), False, False)
        for bin_path in pack.bin_paths:
            print(f"  {pack.name} @ {pack.version}: {bin_path}")
            # use copy_tree from distutils because shutil.copytree stops if directory already exists
            # and therefore can't work in this for loop construction
            try:
                copied += copy_tree(bin_path, deploy_dir)
            except distutils.errors.DistutilsFileError:  # Found a package that defines a bin dir that does not exist
                pass

    click.echo(click.style('Files copied', fg='cyan'))
    for elem in copied:
        print(f"  {PurePath(elem).name}")
