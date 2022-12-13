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

from distutils.dir_util import copy_tree
import distutils.errors
from pathlib import PurePath

import click

from .lockfile import LockFileReader
from .buildinfo import Package


def deploy_all_dependencies(deploy_dir, only_runtime_deps):
    reader = LockFileReader()
    reader.parse()

    click.echo(click.style('Dependencies with bin dirs:', fg='cyan'))
    copied = []
    for dep in reader.all_dependencies:
        pack = Package(dep['library'], dep['version'], dep['package_path'], dep.get('options', []), False, False)

        if only_runtime_deps:
            if dep.get('dependency_type') != "runtime" and dep.get('type') != "runtime":
                continue

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
