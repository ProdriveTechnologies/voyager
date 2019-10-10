from tqdm import tqdm
from artifactory import ArtifactoryPath
import click
import time
import random

VERSION = "0.0.0"

from voyagerfile import VoyagerFile
from generators.visualstudio import VisualStudioGenerator
from buildinfo import BuildInfo
from configfile import ConfigFile
from artifactdownloader import ArtifactDownloader


@click.group()
def cli():
    pass

@cli.command()
@click.argument('repo')
@click.argument('query')
def search(repo, query):
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}/{repo}/"
    path = ArtifactoryPath(art_url, apikey=conf.api_key)
    for p in path.glob(query):
        print(p)
        print(type(p))


@cli.command()
def upload():
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}/siatd-generic-local/API/PA.VirtualMachine/2.0.0/{conf.default_arch}/"
    path = ArtifactoryPath(art_url, apikey=conf.api_key)
    path.mkdir(exist_ok=True)
    path.deploy_file("voyager_package.tgz")

@cli.command()
def install():
    file = VoyagerFile("voyager.json")
    file.parse()
    # file.print()
    down = ArtifactDownloader(file.libraries)
    build_info = down.download()
    gen = VisualStudioGenerator(build_info)
    c = gen.content
    # print(c)
    with open('voyager.props', 'w') as f:
        f.write(c)

@cli.command()
def config():
    conf = ConfigFile()
    print("Key: ", conf.api_key)
    print("URL: ", conf.artifactory_url)
    print("ARCH:", conf.default_arch)

@cli.command()
def init():
    VoyagerFile.generate_empty_file()

if __name__ == "__main__":
    print(f"Voyager version {VERSION}")
    cli()
