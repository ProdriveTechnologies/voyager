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

import importlib
import pkgutil
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import List, Type

import click
import semver

import voyager_plugins
import voyager.voyager
from voyager.Singleton import SingletonType
from voyager.artifactdownloader import ArtifactDownloader
from voyager.plugin_interfaces import Interface, Plugin

class Registry(metaclass=SingletonType):
    """
    Plugin manager.

    Plugin registration happens here, and you can poke the on_x methods to
    trigger event handlers in the registered plugins.
    """

    class RegistryInterface(Interface):
        def __init__(self, registry):
            self.registry: Registry = registry

        @property
        def plugins(self) -> List[Plugin]:
            return list(self.registry.plugins)

        def add_command(self, name=None, cls=None, **attrs) -> click.Command:
            return voyager.voyager.cli.command(name, cls, **attrs)

        def find_versions_for_package(self, repo, library, override_archs) -> List[semver.SemVer]:
            downloader = ArtifactDownloader([], False, False)
            version_strings = downloader.find_versions_for_package(repo, library, override_archs)
            return [semver.make_semver(version, False) for version in version_strings]

    def __init__(self):
        super().__init__()
        self.plugins: List[Plugin] = []
        self._interface = Registry.RegistryInterface(self)

    def reset(self):
        """Reset the plugin registry. Only for test usage."""
        self.plugins = []

    def register(self, plugin: Plugin):
        """
        Add a plugin to the registry.

        All registered plugins will be notified of events.
        """
        self.plugins.append(plugin)

    @property
    def interface(self) -> Interface:
        return self._interface

    def on_install_start(self):
        for plugin in self.plugins:
            plugin.on_install_start()

    def on_install_end(self):
        for plugin in self.plugins:
            plugin.on_install_end()

#
# Plugin loading tools. Borrowed from:
# - https://packaging.python.org/guides/creating-and-discovering-plugins/
# - https://github.com/pyinstaller/pyinstaller/issues/1905#issuecomment-525221546
#

def iter_namespace(ns_pkg):
    """Pyinstaller-compatible namespace iteration.

    Yields the name of all modules found at a given Fully-qualified path.

    To have it running with pyinstaller, it requires to ensure a hook inject the
    "hidden" modules from your plugins folder inside the executable:

    - if your plugins are under the ``myappname/pluginfolder`` module
    - create a file ``specs/hook-<myappname.pluginfolder>.py``
    - content of this file should be:

        .. code-block:: python

            from PyInstaller.utils.hooks import collect_submodules
            hiddenimports = collect_submodules('<myappname.pluginfolder>')
    """
    prefix = ns_pkg.__name__ + "."
    for p in pkgutil.iter_modules(ns_pkg.__path__, prefix):
        yield p[1]


def load_plugin(plugin: Type[Plugin]):
    iface_version = Registry().interface.VERSION
    if semver.satisfies(iface_version, plugin.REQUIRED_INTERFACE_VERSION):
        Registry().register(plugin(Registry().interface))
    else:
        print(f"Not loading plugin {plugin} - version mismatch "
              + f"(required {plugin.REQUIRED_INTERFACE_VERSION}, actual {iface_version}")


def load_plugins():
    """
    Load plugins by importing all packages in the voyager_plugins namespace.
    """
    for name in iter_namespace(voyager_plugins):
        plugin = importlib.import_module(name).Plugin
        load_plugin(plugin)
