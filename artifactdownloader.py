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
        self.build_info = BuildInfo()
    
    def clear_directory(self):
        try:
            shutil.rmtree(self._download_dir)
        except OSError as e:
            print(f'Error: {self._download_dir} : {e.strerror}')

    def make_directory(self):
        p = Path(self._download_dir)
        p.mkdir()

    def download(self):
        self._download(self.libraries, 0)
        return self.build_info
    
    def _download(self, libs, level):
        level_str = self._format_level(level)
        for lib in libs:
            click.echo(f"{level_str} Downloading {lib['library']} @ {lib['version']} ... ", nl=False)

            if lib['library'] in self.build_info.package_names:
                pack = self.build_info.get_package(lib['library'])
                if pack.version != lib['version']:
                    raise ValueError(f"Version conflict for {lib['library']}: {pack.version} vs {lib['version']}")
                click.echo(click.style(u'SKIP', fg='green'))
                continue

            extract_dir = self._find_download_extract_package(lib['repo'], lib['library'], lib['version'])
            
            options = []
            if 'options' in lib:
                options = lib['options']

            # Pass along absolute path for the package so there are no problems with subdirectory projects
            pack = Package(lib['library'], lib['version'], os.path.abspath(extract_dir) + "/", options)
            self.build_info.add_package(pack)
            click.echo(click.style(u'OK', fg='green'))

            self._download(pack.compile_dependencies, level+1)

    def _find_download_extract_package(self, repo, library, version):
        archs = self.config.current_archs
        archs.append("Header")
        found = False
        path = None
        package_dir = ""
        for arch in archs:
            package_dir = f"{repo}/{library}/{version}/{arch}"
            url = f"{self.config.artifactory_url}/{package_dir}/voyager_package.tgz"
            path = ArtifactoryPath(url, apikey=self.config.api_key)

            if path.exists():
                click.echo(click.style(f'{arch} ', fg='bright_blue'), nl=False)
                found = True
                break

        if not found:
            click.echo(click.style(u'ERROR: package not found', fg='red'))
            raise ValueError(f"Package {library} @ {version} not found")

        extract_dir = f"{self._download_dir}/{package_dir}/"
        
        with path.open() as fd:
            tar = tarfile.open(fileobj=fd)
            tar.extractall(extract_dir)

        return extract_dir

    def _format_level(self, level):
        s = "├"
        if level > 0:
            s = "|"
        for x in range(level):
            s  += "   "
        if level > 0:
            s += "└─"
        else:
            s += "──"
        return s


