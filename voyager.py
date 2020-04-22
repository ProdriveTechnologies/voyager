from sys import exit # For generated executables
from artifactory import ArtifactoryPath
import click
import time
import random
import json
from pathlib import Path

VERSION = "1.10.1"

from voyagerfile import VoyagerFile
from generators.visualstudio import VisualStudioGenerator
from generators.cmake import CMakeGenerator, CMakeProjectGenerator
from generators.headercheck import HeaderCheckGenerator
from buildinfo import BuildInfo
from configfile import ConfigFile
from artifactdownloader import ArtifactDownloader
from lockfile import LockFileWriter, LockFileReader
from voyagerpackagefile import VoyagerPackageFile
from cmakepackagefile import CMakePackageFile

@click.group()
def cli():
    """This function is always called before any other command function"""
    conf = ConfigFile()
    if not conf.exists():
        click.echo(click.style(f'It appears that there is no config file in {conf.file_path}', fg='yellow'))
        click.echo("Generating a default one")
        conf.create_default()
        click.echo(click.style(u'Default one generated, please fill in you Artifactory API key', fg='red'))
        exit(1)

    if not conf.parse():
        click.echo(click.style(f'Problem with parsing the config file {conf.file_path}', fg='red'))
        exit(1)

@cli.command()
@click.argument('query')
def search(query):
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}/siatd-generic-local/"
    path = ArtifactoryPath(art_url, apikey=conf.api_key)
    for p in path.glob(query):
        print(p)

def generate_project(generators: list, subdir: str, build_info: BuildInfo):
    """Generate dependency files for each project"""

    supported_generators = {
        'msbuild': ('voyager.props', VisualStudioGenerator),
        'cmake': ('voyager.cmake', CMakeProjectGenerator),
        'headercheck': ('voyager.includes', HeaderCheckGenerator)
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
def install(host, host_file):
    conf = ConfigFile()
    if host:
        conf.set_host_platform(host)
    if host_file:
        conf.set_host_platform_file(host_file)

    if host or host_file:
        print(f"Setting host platform to: {conf.host_platform}")

    # First download the global dependencies
    click.echo(click.style('Top level:', fg='cyan'))
    file = VoyagerFile("voyager.json")
    file.parse()
    down = ArtifactDownloader(file.libraries, False)
    down.clear_directory()
    down.make_directory()

    build_info_global = BuildInfo()
    build_info_global.add_build_info(down.download(build_info_global))

    if file.has_build_tools():
        click.echo(click.style('Top level (build_tools):', fg='cyan'))
        down = ArtifactDownloader(file.build_tools, True)
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
        down = ArtifactDownloader(subdir_file.libraries, False)
        build_info_subdir = down.download(build_info_combined)

        if file.has_build_tools():
            click.echo(click.style(f'{subdir} (build_tools):', fg='cyan'))
            down = ArtifactDownloader(subdir_file.build_tools, True)
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

    l = LockFileWriter()
    l.save()

@cli.command()
@click.argument('template_filename')
def package(template_filename):
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
    conf = ConfigFile()
    print("Location: ", conf.file_path)
    print("Key: ", conf.api_key)
    print("URL: ", conf.artifactory_url)
    print("ARCH:", conf.build_platform)

@cli.command()
def init():
    VoyagerFile.generate_empty_file()

if __name__ == "__main__":
    print(f"Voyager version {VERSION}")
    try:
        cli()
    except ValueError as v:
        click.echo(f"Error during execution of voyager: {v}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error during execution of voyager: {e}", err=True)
        exit(2)
