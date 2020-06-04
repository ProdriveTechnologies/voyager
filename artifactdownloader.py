import shutil
import tarfile
import os
import click
from pathlib import Path
from artifactory import ArtifactoryPath
from semver import valid_range, max_satisfying

from buildinfo import Package, BuildInfo
from configfile import ConfigFile
from lockfile import LockFileWriter

class ArtifactDownloader:
    _download_dir = '.voyager'
    def __init__(self, libraries: list, are_build_tools: bool):
        self.libraries = libraries
        self.config = ConfigFile()
        self.build_info = BuildInfo()
        self.build_tools = are_build_tools

    def clear_directory(self):
        try:
            shutil.rmtree(self._download_dir)
        except OSError as e:
            print(f'Error: {self._download_dir} : {e.strerror}')

    def make_directory(self):
        p = Path(self._download_dir)
        p.mkdir()

    def download(self, build_info_combined):
        self._download(self.libraries, 0, build_info_combined)
        return self.build_info

    def _download(self, libs, level, build_info_combined):
        level_str = self._format_level(level)
        for lib in libs:
            click.echo(f"{level_str} Downloading {lib['library']} @ {lib['version']} ... ", nl=False)

            version_to_download = lib['version']
            override_archs = lib.get('override_archs', None)
            for_archs = lib.get('for_archs', None)
            download_only = lib.get('download_only', None)
            if download_only:
                click.echo(click.style(u'Download only ', fg='green'), nl=False)

            active_archs = self._get_active_archs()
            if for_archs:
                if not any(a in active_archs for a in for_archs):
                    click.echo(click.style(u'SKIP: arch not active', fg='yellow'))
                    continue

            # The version can either be semver or something like feature/xyz when referencing an Rxx version
            # When version is semver, parse and check which versions comply
            # otherwise use the feature/xyz name to download
            if self._check_if_valid_semver(lib['version']):
                versions = self._find_versions_for_package(lib['repo'], lib['library'], override_archs)
                version_to_download = max_satisfying(versions, lib['version'], True)
                if not version_to_download:
                    click.echo(click.style(f"ERROR: version {lib['version']} not found.", fg='red'))
                    click.echo(click.style(f"Available: {versions}", fg='red'))
                    raise ValueError("Version not found")

            # Handle version conflicts within project
            if not download_only and lib['library'] in self.build_info.package_names:
                pack = self.build_info.get_package(lib['library'])
                if pack.version != version_to_download:
                    click.echo(click.style(f"ERROR: Version conflict within project for {lib['library']}: {pack.version} vs {version_to_download}", fg='red'))
                    raise ValueError("Version conflict")
                click.echo(click.style(u'SKIP: package already included in project', fg='green'))
                continue

            # Handle version conflicts between multiple projects or with top level
            if not download_only and lib['library'] in build_info_combined.package_names:
                pack = build_info_combined.get_package(lib['library'])
                if pack.version != version_to_download:
                    click.echo(click.style(f"ERROR: Version conflict between multiple projects or with top level for {lib['library']}: {pack.version} vs {version_to_download}", fg='red'))
                    raise ValueError("Version conflict")
                # Packages that were included in other projects with the same version are added to the build_info without downloading them again
                click.echo(click.style(f"SKIP: package included from other project", fg='green'))
                self.build_info.add_package(pack)
                continue

            extract_dir = self._find_download_extract_package(lib['repo'], lib['library'], version_to_download, lib.get('output_dir', None), override_archs)
            options = []
            if 'options' in lib:
                options = lib['options']

            if download_only:
                click.echo(click.style(u'OK', fg='green'))
                continue

            # Pass along absolute path for the package so there are no problems with subdirectory projects
            pack = Package(lib['library'], version_to_download, os.path.abspath(extract_dir) + "/", options, self.build_tools)
            self.build_info.add_package(pack)

            if level == 0:
                lib['version'] = version_to_download
                l = LockFileWriter()
                l.add_dependency(lib)

            click.echo(click.style(u'OK', fg='green'))

            # This is a recursive function that download dependencies
            # Each recursion the level is incremented for indentation printing
            self._download(pack.compile_dependencies, level+1, build_info_combined)

    def _check_if_valid_semver(self, version):
        """ Check if a string is parseable by the semver library """
        r = valid_range(version, True)
        if r:
            return True
        return False

    def _find_versions_for_package(self, repo, library, override_archs):
        """
        Find the versions for a specific package
        :param repo: The repository, for example siatd-generic-local
        :param library: The name of the library, for example PA.JtagProgrammer
        :returns: A list of strings with versions: ['17.0.0', '18.0.0']
        """
        if override_archs:
            archs = override_archs
        else:
            archs = self._get_active_archs()
        versions = []
        
        path = ArtifactoryPath(self.config.artifactory_url, apikey=self.config.api_key)

        args = [
            "items.find",
            {
                "$and": [
                    {"repo": {"$eq": repo}},
                    {"path": {"$match": f"{library}/*"}},
                ]
            },
        ]

        artifacts_list = path.aql(*args)

        for l in artifacts_list:
            p = l['path'].split('/')
            if p[-1] in archs:
                if self._check_if_valid_semver(p[-2]):
                    versions.append(p[-2])

        return versions

    def _find_download_extract_package(self, repo, library, version, output_dir, override_archs):
        """
        Find, download and extract a package
        :param repo: The repository, for example siatd-generic-local
        :param library: The name of the library, for example PA.JtagProgrammer
        :param version: The version of the library, for example 17.0.0
        :returns: Relative directory to where the package is extracted
        :raises ValueError: When the package could not be found
        """
        if override_archs:
            archs = override_archs
        else:
            archs = self._get_active_archs()
        found = False
        path = None
        package_dir = ""
        for arch in archs:
            package_dir = f"{repo}/{library}/{version}/{arch}"
            url = f"{self.config.artifactory_url}/{package_dir}/voyager_package.tgz"
            path = ArtifactoryPath(url, apikey=self.config.api_key)

            if path.exists():
                click.echo(click.style(f'{arch} @ {version} ', fg='bright_blue'), nl=False)
                found = True
                break

        if not found:
            click.echo(click.style(u'ERROR: package not found', fg='red'))
            raise ValueError(f"Package {library} @ {version} not found")

        if output_dir:
            extract_dir = output_dir
        else:
            extract_dir = f"{self._download_dir}/{package_dir}/"

        if 'deprecated' in path.properties:
            message = path.properties['deprecated']
            click.echo(click.style(f'DEPRECATED: {message} ', fg='yellow'), nl=False)

        with path.open() as fd:
            tar = tarfile.open(fileobj=fd)
            tar.extractall(extract_dir)

        return extract_dir

    def _format_level(self, level):
        """ Return characters based on the level for tree view """
        s = "+"
        if level > 0:
            s = "|"
        for x in range(level):
            s  += "   "
        if level > 0:
            s += "+-"
        else:
            s += "--"
        return s

    def _get_active_archs(self):
        archs = []
        if self.build_tools:
            archs = self.config.build_platform
        else:
            archs = self.config.host_platform
        archs.append("Header")
        archs.append("Source")

        return archs
