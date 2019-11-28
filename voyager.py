from sys import exit # For generated executables
from artifactory import ArtifactoryPath
import click
import time
import random
import json
from pathlib import Path

VERSION = "1.4.1"

from voyagerfile import VoyagerFile
from generators.visualstudio import VisualStudioGenerator
from buildinfo import BuildInfo
from configfile import ConfigFile
from artifactdownloader import ArtifactDownloader
from lockfile import LockFileWriter, LockFileReader
from voyagerpackagefile import VoyagerPackageFile

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

@cli.command()
def install():
    # First download the global dependencies
    file = VoyagerFile("voyager.json")
    file.parse()
    down = ArtifactDownloader(file.libraries)
    down.clear_directory()
    down.make_directory()

    click.echo(click.style('Top level:', fg='cyan'))
    build_info_global = down.download()

    for subdir in file.projects:
        click.echo(click.style(f'{subdir}:', fg='cyan'))
        subdir_file = VoyagerFile(f"{subdir}/voyager.json")
        subdir_file.parse()
        down = ArtifactDownloader(subdir_file.libraries)
        build_info_subdir = down.download()
        build_info_subdir.add_build_info(build_info_global)
        gen = VisualStudioGenerator(build_info_subdir)
        c = gen.content
        with open(f"{subdir}/voyager.props", 'w') as f:
            f.write(c)
        # Find project file and touch it to force reload in Visual Studio
        for p in (Path.cwd() / subdir).glob('*.vcxproj'):
            p.touch()
    
    # When working on a single project file
    if file.type == "project":
        gen = VisualStudioGenerator(build_info_global)
        c = gen.content
        with open(f"voyager.props", 'w') as f:
            f.write(c)
        # Find project file and touch it to force reload in Visual Studio
        for p in (Path.cwd() / subdir).glob('*.vcxproj'):
            p.touch()

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
    print("ARCH:", conf.default_archs)

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
    
