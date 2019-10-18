import shutil
import tarfile
import click
from pathlib import Path
from artifactory import ArtifactoryPath

from buildinfo import Package, BuildInfo
from configfile import ConfigFile

class ArtifactDownloader:
    _download_dir = 'libs'
    def __init__(self, libraries):
        self.libraries = libraries
        self.config = ConfigFile()
    
    def clear_directory(self):
        try:
            shutil.rmtree(self._download_dir)
        except OSError as e:
            print(f'Error: {self._download_dir} : {e.strerror}')

    def make_directory(self):
        p = Path(self._download_dir)
        p.mkdir()

    def download(self):
        self.clear_directory()
        self.make_directory()
        # deps = Dependencies()
        build = BuildInfo()

        for lib in self.libraries:
            click.echo(f"Downloading {lib['library']} @ {lib['version']} ... ", nl=False)
            
            package_dir = f"{lib['repo']}/{lib['library']}/{lib['version']}/{self.config.current_arch}"
            url = f"{self.config.artifactory_url}/{package_dir}/voyager_package.tgz"
            path = ArtifactoryPath(url, apikey=self.config.api_key)

            if not path.exists():
                package_dir = f"{lib['repo']}/{lib['library']}/{lib['version']}/SRC"
                url = f"{self.config.artifactory_url}/{package_dir}/voyager_package.tgz"
                path = ArtifactoryPath(url, apikey=self.config.api_key)
                if not path.exists():
                    click.echo(click.style(u'ERROR: package not found', fg='red'))
                    exit(1)

            extract_dir = f"{self._download_dir}/{package_dir}/"
            
            with path.open() as fd:
                tar = tarfile.open(fileobj=fd)
                tar.extractall(extract_dir)
            
            pack = Package(lib['library'], extract_dir)
            build.add_package(pack)
            click.echo(click.style(u'OK', fg='green'))
        
        return build
