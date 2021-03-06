# Copyright 2021 Prodrive Technologies
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

from abc import ABC, abstractmethod, abstractproperty
from typing import List

import click
import semver

class Plugin:
    """
    The interface a voyager plugin should implement.

    Plugins don't have to inherit from it, but all Plugin methods must be defined.
    """

    # Default compatibility is with nothing, so you have to set this in a plugin.
    REQUIRED_INTERFACE_VERSION = semver.Range("0.0.0", False)

    # Version identifier of the plugin, set this in the plugin
    PLUGIN_VERSION = "Undefined version"

    def __init__(self, interface):
        self.interface: Interface = interface

    def on_install_start(self):
        """Called whenever voyager install starts."""
        pass

    def on_install_end(self):
        """Called when voyager install finishes."""
        pass

    def __str__(self):
        return f"{type(self).__name__} - {self.PLUGIN_VERSION}"


class Interface(ABC):
    """The interface passed to plugins through which they should make calls into voyager."""

    VERSION = semver.SemVer("0.1.2", False)

    @abstractproperty
    def plugins(self) -> List[Plugin]:
        """Get a list of all currently loaded plugins."""
        pass

    @abstractmethod
    def add_command(self, name=None, cls=None, **attrs) -> click.Command:
        """
        Add a command to voyager.

        This is routed directly to click.command; see its documentation for more
        details.
        """
        pass

    @abstractmethod
    def find_versions_for_package(self, repo, library, override_archs) -> List[semver.SemVer]:
      """
      Get a list of available versions for a particular package.

      Internally, this delegates to ArtifactDownloader and uses the same auth
      information.
      """
      pass

    @abstractmethod
    def get_version(self) -> str:
        """Get the current version number of voyager"""
        pass

    @abstractmethod
    def get_artifactory_url(self) -> str:
        """Get the artifactory url from the config file"""
        pass
