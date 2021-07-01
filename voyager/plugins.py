import importlib
import pkgutil
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import List, Type

import click
import semver

from voyager.Singleton import SingletonType
from voyager import voyager


class Plugin:
    """
    The interface a voyager plugin should implement.

    Plugins don't have to inherit from it, but all Plugin methods must be defined.
    """

    # Default compatibility is with nothing, so you have to set this in a plugin.
    REQUIRED_INTERFACE_VERSION = semver.Range("0.0.0", False)

    def __init__(self, interface):
        self.interface: Interface = interface

    def on_start(self):
        pass

    def on_end(self):
        pass

    def __str__(self):
        return type(self).__name__


class Interface(ABC):
    """The interface passed to plugins through which they should make calls into voyager."""

    VERSION = semver.SemVer("0.1.0", False)

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
            return voyager.cli.command(name, cls, **attrs)

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

    def on_start(self):
        for plugin in self.plugins:
            plugin.on_start()

    def on_end(self):
        for plugin in self.plugins:
            plugin.on_end()


def load_plugin(plugin: Type[Plugin]):
    iface_version = Registry().interface.VERSION
    if semver.satisfies(iface_version, plugin.REQUIRED_INTERFACE_VERSION):
        Registry().register(plugin(Registry().interface))
    else:
        print(f"Not loading plugin {plugin} - version mismatch "
              + f"(required {plugin.REQUIRED_INTERFACE_VERSION}, actual {iface_version}")


def load_plugins():
    """
    Load plugins by importing all packages that start with "voyager_".

    Borrowed from https://packaging.python.org/guides/creating-and-discovering-plugins/

    Big TODO: provide diagnostic info when importing or registration fails
    """
    for finder, name, ispkg in pkgutil.iter_modules():
        if (name.startswith("voyager_")):
            plugin = importlib.import_module(name).Plugin
            load_plugin(plugin)
