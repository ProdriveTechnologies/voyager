# Copyright 2022 Prodrive Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from voyager.artifactdownloader import ArtifactDownloader
from voyager.voyagerfile import VoyagerFile
import semver
import click

from typing import List


def execute_package_update():
    click.echo(click.style('Top level:', fg='cyan'))
    file = VoyagerFile("voyager.json")
    file.parse()

    check_for_updates(file.libraries)

    if file.has_build_tools():
        click.echo(click.style('Top level (build_tools):', fg='cyan'))
        check_for_updates(file.build_tools)

    for subdir in file.projects:
        click.echo(click.style(f'{subdir}:', fg='cyan'))
        subdir_file = VoyagerFile(f"{subdir}/voyager.json")
        subdir_file.parse()

        check_for_updates(subdir_file.libraries)

        if subdir_file.has_build_tools():
            click.echo(click.style(f'{subdir} (build_tools):', fg='cyan'))
            check_for_updates(subdir_file.build_tools)


def check_for_updates(libraries_or_build_tools):
    updates_proposed = False
    down = ArtifactDownloader(libraries_or_build_tools, False, False)

    for lib in libraries_or_build_tools:
        # When not a valid semver continue with the next item
        if not down.check_if_valid_semver(lib['version']):
            continue

        # Find out the available versions in Artifactory and which one would be downloaded for the given range
        available_package_versions = down.find_versions_for_package(lib['repo'], lib['library'], None)
        version_to_download_str = semver.max_satisfying(available_package_versions, lib['version'], True)

        if not version_to_download_str:
            continue

        # Make a list of every version that is higher
        higher_versions = []
        for version_str in available_package_versions:
            if semver.lt(version_to_download_str, version_str, False):
                higher_versions.append(version_str)

        # when no higher versions continue with next lib
        if len(higher_versions) == 0:
            continue

        updates_proposed = True

        # combine patch versions to only include highest
        higher_versions = semver_reduce_patch(higher_versions)

        # Print results
        click.echo(f"  Update available for: ", nl=False)
        click.echo(click.style(f"{lib['library']}", fg='bright_blue'), nl=False)
        click.echo(f" - {lib['version']} @ {version_to_download_str}")

        for higher_version in higher_versions:
            diff = semver_diff(version_to_download_str, higher_version)

            if diff == "major":
                click.echo(click.style(f'    Major: {higher_version}', fg='bright_green'), nl=False)
            elif diff == "minor":
                click.echo(click.style(f'    Minor: {higher_version}', fg='bright_magenta'), nl=False)
            elif diff == "patch":
                click.echo(click.style(f'    Patch: {higher_version}', fg='bright_cyan'), nl=False)
            else:
                click.echo(click.style(f'    ?????: {higher_version}', fg='bright_red'), nl=False)

            proposed_version_str = get_recommended_version_str(higher_version)
            click.echo(f" - set voyager.json to {proposed_version_str}")

    if not updates_proposed:
        click.echo("  No updates")

def get_recommended_version_str(version: str) -> str:
    """Construct a recommended version string (major.minor) for the voyager.json"""
    ver = semver.semver(version, False)
    return f"\"version\": \"{ver.major}.{ver.minor}\""


def semver_reduce_patch(versions: List[str]) -> List[str]:
    """
    Reduce the patch versions in a list to only the highest
    :param versions: A list of strings with versions ['17.0.0', '18.0.0', '18.0.1']
    :returns: A list of strings with versions: ['17.0.0', '18.0.1']
    """
    reduce_dict = {}
    for version_str in versions:
        version = semver.semver(version_str, False)
        major_minor_str = F"{version.major}.{version.minor}"

        if major_minor_str in reduce_dict:
            if reduce_dict[major_minor_str] < version.minor:
                reduce_dict[major_minor_str] = version.minor
        else:
            reduce_dict[major_minor_str] = version.minor

    results = []
    for key, value in reduce_dict.items():
        results.append(F"{key}.{value}")

    return results


def semver_diff(a: str, b: str) -> str:
    """Compare 2 semver strings and return the difference in a string"""
    if a == b:
        return "same"

    v1 = semver.parse(a, False)
    v2 = semver.parse(b, False)

    if v1.major != v2.major:
        return "major"

    if v1.minor != v2.minor:
        return "minor"

    if v1.patch != v2.patch:
        return "patch"


