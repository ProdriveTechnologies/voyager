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

# System imports
from sys import exit # For generated executables
from pathlib import Path
import logging

# pip imports
import click
import semver

# local imports
from .voyagerfile import VoyagerFile
from .generators.visualstudio import VisualStudioGenerator
from .generators.cmake import CMakeGenerator, CMakeProjectGenerator
from .generators.headercheck import HeaderCheckGenerator
from .generators.packagelist import PackageListGenerator
from .buildinfo import BuildInfo
from .configfile import ConfigFile
from .artifactdownloader import ArtifactDownloader
from .lockfile import LockFileWriter, LockFileReader
from .voyagerpackagefile import VoyagerPackageFile
from .cmakepackagefile import CMakePackageFile
import voyager.artifactorysearch as artifactorysearch
import voyager.deployfromlockfile as deployfromlockfile
import voyager.artifactorylogin as artifactorylogin
import voyager.plugin_registry as plugin_registry
import voyager.doc as doc_server

VERSION = "1.15.0"


@click.group()
def cli():
    """The Voyager package manager.

    Voyager can be used to install binary or source packages from Artifactory,
    and configure your build to integrate them. For more info about individual
    actions, see https://prodrivetechnologies.github.io/voyager/ or

      voyager <action> --help
    """
    conf = ConfigFile()
    if not conf.exists():
        click.echo(click.style(f'It appears that there is no config file in {conf.file_path}', fg='yellow'))
        click.echo("Generating a default one")
        conf.create_default()
        click.echo(click.style(u'Default one generated, please fill in your Artifactory API key or use \'voyager login\'', fg='black', bg='yellow'))
        exit(1)

    if not conf.parse():
        click.echo(click.style(f'Problem with parsing the config file {conf.file_path}', fg='red'))
        exit(1)

@cli.command()
@click.argument('query')
def search(query):
    """Search for a specific package. For example: voyager search Udsm* or voyager search Utils/* """
    ConfigFile.check_for_valid_api_key()
    split = query.split('/')
    if len(split) == 1:
        found = artifactorysearch.gavc(artifact_id=query)
    elif len(split) == 2:
        found = artifactorysearch.gavc(group_id=f"{split[0]}*", artifact_id=split[1])
    else:
        raise ValueError(f"Search query: {query} is not supported")

    for key, values in found.items():
        valid_semvers = []
        for version in values:
            if semver.valid_range(version, True):
                valid_semvers.append(version)

        latest_version = semver.max_satisfying(valid_semvers, "*", False)
        print(f"{key}/{latest_version} {values}")

@cli.command()
@click.argument('library_string')
@click.option('--force-version', '-ff', default=False, help='Add force version attribute', is_flag=True)
def add(library_string, force_version):
    """Add a library to the working directory voyager.json and save it.

    The library_string must use the following format: example-generic-local/Utils/Exceptions/1.2.0
    """
    file = VoyagerFile("voyager.json")
    file.parse()

    file.add_library(library_string, force_version)

def generate_project(generators: list, subdir: str, build_info: BuildInfo):
    """Generate dependency files for each project"""

    supported_generators = {
        'msbuild': ('voyager.props', VisualStudioGenerator),
        'cmake': ('voyager.cmake', CMakeProjectGenerator),
        'headercheck': ('voyager.includes', HeaderCheckGenerator),
        'packagelist': ('voyager.h', PackageListGenerator)
    }

    for name in generators:
        if not name in supported_generators:
            raise ValueError(
                'Unsupported generator "{}". Supported generators are: {}.'.format(
                name, ", ".join(supported_generators.keys())))
        filename, generator = supported_generators[name]
        gen = generator(build_info)
        with open(f"./{subdir}/{filename}", 'w') as f:
            f.write(gen.content)

    # Find project file and touch it to force reload in Visual Studio
    subdir_path = Path.cwd() / subdir
    for p in subdir_path.glob('*.vcxproj'):
        p.touch()

@cli.command()
@click.option('--host', default=None, help='Host platform for cross compilation')
@click.option('--host-file', default=None, help='File with host platforms for cross compilation')
@click.option('--with-runtime-deps', '-wrd', default=False, help='Install runtime dependencies', is_flag=True)
def install(host, host_file, with_runtime_deps):
    """Install packages according to voyager.json.

    The voyager.json in the working directory is assumed to be the top-level
    configuration file. If 'type' is 'solution', the folders listed in
    'projects' are also processed.
    """
    ConfigFile.check_for_valid_api_key()
    plugin_registry.Registry().on_install_start()
    conf = ConfigFile()
    if host:
        conf.set_host_platform(host)
    if host_file:
        conf.set_host_platform_file(host_file)

    if host or host_file:
        print(f"Setting host platform to: {conf.host_platform}")

    overlay_file = None

    if Path("voyager.overlay.json").is_file():
        click.echo(click.style('Overlay file active', fg='yellow'))
        overlay_file = VoyagerFile("voyager.overlay.json")
        overlay_file.parse()

    # First download the global dependencies
    click.echo(click.style('Top level:', fg='cyan'))
    file = VoyagerFile("voyager.json")
    file.parse()
    file.combine_with_overlay(overlay_file)

    down = ArtifactDownloader(file.libraries, False, with_runtime_deps)
    down.clear_directory()
    down.make_directory()

    build_info_global = BuildInfo()
    build_info_global.add_build_info(down.download(build_info_global))

    if file.has_build_tools():
        click.echo(click.style('Top level (build_tools):', fg='cyan'))
        down = ArtifactDownloader(file.build_tools, True, with_runtime_deps)
        build_info_tools = down.download(build_info_global)
        build_info_global.add_build_info(build_info_tools)

# Build_info_global holds the toplevel build_info only
# build_info_combined is everything summed up of top level and all subdirs
    build_info_combined = BuildInfo()
    build_info_combined.add_build_info(build_info_global)

    for subdir in file.projects:
        click.echo(click.style(f'{subdir}:', fg='cyan'))
        subdir_file = VoyagerFile(f"{subdir}/voyager.json")
        subdir_file.parse()
        subdir_file.combine_with_overlay(overlay_file)
        down = ArtifactDownloader(subdir_file.libraries, False, with_runtime_deps)
        build_info_subdir = down.download(build_info_combined)

        if file.has_build_tools():
            click.echo(click.style(f'{subdir} (build_tools):', fg='cyan'))
            down = ArtifactDownloader(subdir_file.build_tools, True, with_runtime_deps)
            build_info_tools = down.download(build_info_combined)
            build_info_subdir.add_build_info(build_info_tools)

        # Add the subdir to Combined so it is up to date
        # Add Global to subdir so generate_project includes top level as well
        build_info_combined.add_build_info(build_info_subdir)
        build_info_subdir.add_build_info(build_info_global)
        generate_project(file.generators, subdir, build_info_subdir)

    # When working on a single project file
    if file.type == "project":
        generate_project(file.generators, "", build_info_global)

    if 'cmake' in file.generators:
        for _, package in build_info_combined.packages:
            cmake_package_file = CMakePackageFile(package)
            cmake_package_file.save()

        gen_cmake_solution = CMakeGenerator(build_info_combined)
        with open('voyager_solution.cmake', 'w') as f:
            f.write(gen_cmake_solution.content)

    # Log statistics
    number_of_packages = len(build_info_combined.packages)
    logging.getLogger('voyager').info(
        f"Installed {number_of_packages} packages", extra={'Packages': number_of_packages})

    l = LockFileWriter()
    l.save()
    plugin_registry.Registry().on_install_end()

@cli.command()
@click.argument('template_filename')
def package(template_filename):
    """Populate a voyager_package.json's "dependencies" section.

    Takes a template file and adds all the current project's public dependencies
    (any with a "dependency_type") to its "dependencies" section.
    """
    l = LockFileReader()
    l.parse()
    l.print()

    p = VoyagerPackageFile(template_filename)
    p.parse_template()
    p.add_dependencies(l.compile_dependencies)
    p.add_dependencies(l.runtime_dependencies)

    p.save()


@cli.command()
def config():
    """Generate a default voyager configuration file in your home dir."""
    conf = ConfigFile()
    print("Location: ", conf.file_path)
    print("Key: ", conf.api_key)
    print("URL: ", conf.artifactory_url)
    print("ARCH:", conf.build_platform)

@cli.command()
def init():
    """Generate a starting point for voyager.json."""
    VoyagerFile.generate_empty_file()

@cli.command()
@click.option('--dir', 'deploy_dir', default=".voyager/.deploy", help='Folder to place the binaries in')
@click.option('--only-runtime-deps', '-ord', default=False, help='Install only runtime dependencies', is_flag=True)
def deploy(deploy_dir, only_runtime_deps):
    """Deploy all binary dependencies to a target folder.

    This command is useful when you have binary dependencies (such as DLLs or
    executables) that are otherwise not available on the target system.
    """
    print("Deploy")
    deployfromlockfile.deploy_all_dependencies(deploy_dir, only_runtime_deps)

@cli.command()
def login():
    """Configure access to Artifactory."""
    print("Login and get Artifactory API key for config file")
    artifactorylogin.login()

@cli.command()
def doc():
    """Run a local website that links to the docs of the individual packages"""
    doc_server.run_doc_server()

def main():
    print(f"Voyager version {VERSION}")

    # On default disable the output of the voyager logger. Use a plugin to enable and make use of custom handlers
    logging.getLogger('voyager').disabled = True
    logging.getLogger('voyager').propagate = False

    try:
        plugin_registry.load_plugins()
        logging.getLogger('voyager').info("Voyager Startup")
        cli()
    except ValueError as v:
        click.echo(f"Error during execution of voyager: {v}", err=True)
        logging.getLogger('voyager').exception(f"ValueError: {v}")
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error during execution of voyager: {e}", err=True)
        logging.getLogger('voyager').exception(f"Unexpected error: {e}")
        exit(2)


if __name__ == "__main__":
    main()
