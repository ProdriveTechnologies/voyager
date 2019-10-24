import shutil
import tarfile
import os
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
        build = BuildInfo()

        for lib in self.libraries:
            click.echo(f"Downloading {lib['library']} @ {lib['version']} ... ", nl=False)
            
            archs = self.config.current_archs
            archs.append("Header")

            found = False
            path = None
            package_dir = ""
            for arch in archs:
                package_dir = f"{lib['repo']}/{lib['library']}/{lib['version']}/{arch}"
                url = f"{self.config.artifactory_url}/{package_dir}/voyager_package.tgz"
                path = ArtifactoryPath(url, apikey=self.config.api_key)

                if path.exists():
                    click.echo(click.style(f'{arch} ', fg='bright_blue'), nl=False)
                    found = True
                    break

            if not found:
                click.echo(click.style(u'ERROR: package not found', fg='red'))
                raise ValueError(f"Package {lib['library']} @ {lib['version']} not found")

            extract_dir = f"{self._download_dir}/{package_dir}/"
            
            with path.open() as fd:
                tar = tarfile.open(fileobj=fd)
                tar.extractall(extract_dir)
            
            # Pass along absolute path for the package so there are no problems with subdirectory projects
            pack = Package(lib['library'], os.path.abspath(extract_dir))
            build.add_package(pack)
            click.echo(click.style(u'OK', fg='green'))
        
        return build
