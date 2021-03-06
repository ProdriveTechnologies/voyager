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
    file = VoyagerFile("voyager.json")
    file.parse()

    update_list = []

    update_list += _check_for_updates(file.libraries)

    if file.has_build_tools():
        update_list += _check_for_updates(file.build_tools)

    for subdir in file.projects:
        subdir_file = VoyagerFile(f"{subdir}/voyager.json")
        subdir_file.parse()

        update_list += _check_for_updates(subdir_file.libraries)

        if subdir_file.has_build_tools():
            update_list += _check_for_updates(subdir_file.build_tools)

    click.echo(click.style("Patch Update ", fg='bright_green'), nl=False)
    click.echo(click.style("Backwards-compatible bug fixes.", fg='green'), nl=True)
    for elem in update_list:
        if elem['update-type'] == "patch":
            click.echo(click.style(f" {elem['library']}".ljust(40), fg='cyan'), nl=False)
            click.echo(f" {elem['version']} -> {elem['new-version']}".ljust(20), nl=False)
            click.echo(f" {elem['proposed']}")

    print("")
    click.echo(click.style("Minor Update ", fg='bright_yellow'), nl=False)
    click.echo(click.style("New backwards-compatible features.", fg='yellow'), nl=True)
    for elem in update_list:
        if elem['update-type'] == "minor":
            click.echo(click.style(f" {elem['library']}".ljust(40), fg='cyan'), nl=False)
            click.echo(f" {elem['version']} -> {elem['new-version']}".ljust(20), nl=False)
            click.echo(f" {elem['proposed']}")

    print("")
    click.echo(click.style("Major Update ", fg='bright_red'), nl=False)
    click.echo(click.style("Potentially breaking API changes, use caution.", fg='red'), nl=True)
    for elem in update_list:
        if elem['update-type'] == "major":
            click.echo(click.style(f" {elem['library']}".ljust(40), fg='cyan'), nl=False)
            click.echo(f" {elem['version']} -> {elem['new-version']}".ljust(20), nl=False)
            click.echo(f" {elem['proposed']}")


def _check_for_updates(libraries_or_build_tools):
    down = ArtifactDownloader(libraries_or_build_tools, False, False)

    update_list = []

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

        # combine patch versions to only include highest
        higher_versions = _semver_reduce_patch(higher_versions)

        for higher_version in higher_versions:
            diff = _semver_diff(version_to_download_str, higher_version)

            proposed_version_str = _get_recommended_version_str(higher_version)

            update_list.append({
                "library": lib['library'],
                "version": version_to_download_str,
                "update-type": diff,
                "new-version": higher_version,
                "proposed": proposed_version_str
            })

    return update_list


def _get_recommended_version_str(version: str) -> str:
    """Construct a recommended version string (major.minor) for the voyager.json"""
    ver = semver.semver(version, False)
    return f"\"version\": \"{ver.major}.{ver.minor}\""


def _semver_reduce_patch(versions: List[str]) -> List[str]:
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
            if reduce_dict[major_minor_str] < version.patch:
                reduce_dict[major_minor_str] = version.patch
        else:
            reduce_dict[major_minor_str] = version.patch

    results = []
    for key, value in reduce_dict.items():
        results.append(F"{key}.{value}")

    return results


def _semver_diff(a: str, b: str) -> str:
    """Compare 2 semver strings and return which part (major/minor/patch) is different in a string"""
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


