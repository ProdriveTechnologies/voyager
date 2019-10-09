import shutil
import tarfile
import click
from pathlib import Path
from artifactory import ArtifactoryPath

from buildinfo import Package, BuildInfo
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
        # deps = Dependencies()
        build = BuildInfo()

        for lib in self.libraries:
            click.echo(f"Downloading {lib['library']} @ {lib['version']} ... ", nl=False)
            url = f"{self.config.artifactory_url}/{lib['repo']}/{lib['library']}/{lib['version']}/{self.config.current_arch}/voyager_package.tgz"
            path = ArtifactoryPath(url, apikey=self.config.api_key)

            if not path.exists():
                url = f"{self.config.artifactory_url}/{lib['repo']}/{lib['library']}/{lib['version']}/SRC/voyager_package.tgz"
                path = ArtifactoryPath(url, apikey=self.config.api_key)
                if not path.exists():
                    click.echo(click.style(u'❌  package not found', fg='red'))
                    exit(1)

            s = str(path)
            s = s.replace(self.config.artifactory_url, "")
            s = s.replace('voyager_package.tgz', "")
            s = self.__download_dir + s
            
            with path.open() as fd:
                tar = tarfile.open(fileobj=fd)
                tar.extractall(s)
            
            pack = Package(lib['library'], s)
            build.add_package(pack)
            click.echo(click.style(u'✔️', fg='green'))
        
        return build
