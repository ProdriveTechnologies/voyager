import shutil
import tarfile
import os
import click
from pathlib import Path
from artifactory import ArtifactoryPath
from semver import valid_range, max_satisfying
import semver

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
        self._download(self.libraries, 0, build_info_combined, False)
        return self.build_info

    def _download(self, libs, level, build_info_combined, runtime_deps):
        level_str = self._format_level(level)
        for lib in libs:
            click.echo(f"{level_str} Downloading {lib['library']} @ {lib['version']} ... ", nl=False)

            version_to_download = lib['version']
            override_archs = lib.get('override_archs', None)
            for_archs = lib.get('for_archs', None)
            download_only = lib.get('download_only', None)
            force_version = lib.get('force_version', False)
            local_path = lib.get('local_path', None)
            overlay_active = lib.get('overlay', False)
            if overlay_active:
                click.echo(click.style('Overlay ', fg='yellow'), nl=False)
            if download_only:
                click.echo(click.style(u'Download only ', fg='green'), nl=False)
            if local_path:
                click.echo(click.style('Local ', fg='magenta'), nl=False)
            if runtime_deps:
                click.echo(click.style('Runtime ', fg='green'), nl=False)
                download_only = True  # Set to download only to skip any version conflict checks

            active_archs = self._get_active_archs()
            if for_archs:
                if not any(a in active_archs for a in for_archs):
                    click.echo(click.style(u'SKIP: arch not active', fg='yellow'))
                    continue

            # The version can either be semver or something like feature/xyz when referencing an Rxx version
            # When version is semver, parse and check which versions comply
            # otherwise use the feature/xyz name to download
            if self._check_if_valid_semver(lib['version']) and not local_path:
                versions = self.find_versions_for_package(lib['repo'], lib['library'], override_archs)
                version_to_download = max_satisfying(versions, lib['version'], True)
                if not version_to_download:
                    click.echo(click.style(f"ERROR: version {lib['version']} not found.", fg='red'))
                    click.echo(click.style(f"Available: {versions}", fg='red'))
                    raise ValueError("Version not found")

            # Handle version conflicts within project
            if not download_only and lib['library'] in self.build_info.package_names:
                pack = self.build_info.get_package(lib['library'])
                self._check_and_handle_dependency_conflict(pack, lib, version_to_download)
                click.echo(click.style(u'SKIP: package already included in project', fg='green'))
                continue

            # Handle version conflicts between multiple projects or with top level
            if not download_only and lib['library'] in build_info_combined.package_names:
                pack = build_info_combined.get_package(lib['library'])
                options = []
                if 'options' in lib:
                    options = lib['options']
                pack.options = options
                self._check_and_handle_dependency_conflict(pack, lib, version_to_download)
                # Packages that were included in other projects with the same version are added to the build_info without downloading them again
                click.echo(click.style(f"SKIP: package downloaded for other project", fg='green'))
                self.build_info.add_package(pack)
            else:

                if local_path:
                    extract_dir = self._find_local_package(lib['library'], local_path, lib.get('output_dir', None))
                else:
                    extract_dir = self._find_download_extract_package(lib['repo'], lib['library'], version_to_download, lib.get('output_dir', None), override_archs)

                if force_version:
                    click.echo(click.style('(Force Version) ', fg='yellow'), nl=False)

                # Set the downloaded version in the Lib object
                lib['version'] = version_to_download
                lib['package_path'] = os.path.abspath(extract_dir) + "/"
                # Write the package to the voyager.lock file
                l = LockFileWriter()
                if level == 0:
                    l.add_library(lib)
                else:
                    l.add_transitive_dependency(lib)

                if download_only:
                    click.echo(click.style(u'OK', fg='green'))
                    continue

                options = []
                if 'options' in lib:
                    options = lib['options']
                # Pass along absolute path for the package so there are no problems with subdirectory projects
                pack = Package(lib['library'], version_to_download, os.path.abspath(extract_dir) + "/", options, self.build_tools, force_version)
                self.build_info.add_package(pack)
    
                click.echo(click.style(u'OK', fg='green'))

            # This is a recursive function that download dependencies
            # Each recursion the level is incremented for indentation printing
            self._download(pack.compile_dependencies, level+1, build_info_combined, runtime_deps)
            self._download(pack.runtime_dependencies, level + 1, build_info_combined, True)

    def _check_and_handle_dependency_conflict(self, pack: Package, lib, version_to_download: str):
        """
        Check for dependency conflicts between 2 versions and handle in case of force version
        :param pack: The package that was originally downloaded and may have force_version set
        :param lib: The library that needs to be downloaded
        :param version_to_download: The resolved version that needs to be downloaded
        :raises ValueError: When a dependency conflict is not resolvable
        """
        if pack.version != version_to_download:
            if not pack.force_version:
                click.echo(click.style(f"ERROR: Version conflict within project for {lib['library']}: {pack.version} vs {version_to_download}", fg='red'))
                raise ValueError("Version conflict")
            else:
                # Check if the forced version is greater
                # when either uses a branch name as the version I consider it a free for all
                # when both semvers are valid we must check that the forced version is newer
                if self._check_if_valid_semver(pack.version) and self._check_if_valid_semver(version_to_download):
                    sem_pack = semver.semver(pack.version, False)
                    sem_down = semver.semver(version_to_download, False)
                    if semver.lt(sem_pack, sem_down, False):  # sem_pack < sem_down
                        click.echo(click.style(f'ERROR: Cannot force {version_to_download} to lower version {pack.version} ', fg='red'))
                        raise ValueError("Version forcing conflict")

                click.echo(click.style(f'WARN: Forcing version {version_to_download} to {pack.version} ', fg='yellow'), nl=False)

    def _check_if_valid_semver(self, version):
        """ Check if a string is parseable by the semver library """
        r = valid_range(version, True)
        if r:
            return True
        return False

    def find_versions_for_package(self, repo, library, override_archs):
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

    def _find_local_package(self, library, local_path, output_dir):
        package_path = Path(local_path)

        if not package_path.exists():
            click.echo(click.style(u'ERROR: local package not found', fg='red'))
            raise ValueError(f"Local package not found")

        if not package_path.is_dir():
            click.echo(click.style(u'ERROR: local package is not a directory', fg='red'))
            raise ValueError(f"Local package not found")

        if output_dir:
            extract_dir = output_dir
            shutil.copytree(local_path, extract_dir)
        else:
            extract_dir = local_path

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
