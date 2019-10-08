import shutil
import tarfile
import click
from pathlib import Path
from artifactory import ArtifactoryPath

from dependencies import Dependency, Dependencies, Package
from configfile import ConfigFile

class ArtifactDownloader:
    __download_dir = 'libs'
    def __init__(self, libraries):
        self.libraries = libraries
        self.config = ConfigFile()
    
    def clear_directory(self):
        try:
            shutil.rmtree(self.__download_dir)
        except OSError as e:
            print(f'Error: {self.__download_dir} : {e.strerror}')

    def make_directory(self):
        p = Path(self.__download_dir)
        p.mkdir()

    def download(self):
        self.clear_directory()
        self.make_directory()
        deps = Dependencies()

        for lib in self.libraries:
            click.echo(f"Downloading {lib['library']} @ {lib['version']} ... ", nl=True)
            url = f"{self.config.artifactory_url}/{lib['repo']}/{lib['library']}/{lib['version']}/{self.config.current_arch}/"
            path = ArtifactoryPath(url, apikey=self.config.api_key)
            for p in path.glob("**/*"):
                s = str(p)
                s = s.replace(self.config.artifactory_url, "")
                s = s.replace('voyager_package.tgz', "")
                s = self.__download_dir + s
                with p.open() as fd:
                    tar = tarfile.open(fileobj=fd)
                    tar.extractall(s)
                pack = Package(lib['library'], s)
                # dep = Dependency(s)
                # deps.update(lib['library'], dep)
                # print(dep.include_paths)

            click.echo(click.style(f'OK', fg='green'))