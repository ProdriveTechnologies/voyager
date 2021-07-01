from .Singleton import SingletonType
from pathlib import Path
from typing import List, Type

from . import voyager

import importlib
import pkgutil
import semver
import click


class Plugin:
    """
    Base for a voyager plugin.

    Plugins don't have to inherit from it, but all Plugin methods must be defined.
    """

    REQUIRED_INTERFACE_VERSION = semver.Range("0.0.0", False)

    @classmethod
    def required_plugin_version(cls) -> semver.Range:
        """Returns the Plugins.INTERFACE_VERSION required for this plugin."""
        return cls.REQUIRED_INTERFACE_VERSION

    def on_start(self):
        pass

    def on_end(self):
        pass

    def __str__(self):
        return type(self).__name__


class Plugins(metaclass=SingletonType):
    """
    Plugin manager.

    Plugin registration happens here, and you can poke the on_x methods to
    trigger event handlers in the registered plugins.
    """

    INTERFACE_VERSION = semver.SemVer("0.1.0", False)

    def __init__(self):
        super().__init__()
        self._plugins: List[Plugin] = []

    def reset(self):
        """Reset the plugin registry. Only for test usage."""
        self._plugins = []

    def register(self, plugin: Plugin):
        """
        Add a plugin to the registry.

        All registered plugins will be notified of events.
        """
        self._plugins.append(plugin)

    # Everything below here is covered under interface versioning

    @property
    def plugins(self) -> List[Plugin]:
        return list(self._plugins)

    def add_command(self, name=None, cls=None, **attrs) -> click.Command:
        """
        Add a command to voyager.

        This is routed directly to click.command; see its documentation for more
        details.
        """

        return voyager.cli.command(name, cls, **attrs)

    def on_start(self):
        for plugin in self.plugins:
            plugin.on_start()

    def on_end(self):
        for plugin in self.plugins:
            plugin.on_end()


def load_plugins():
    """
    Load plugins by importing all packages that start with "voyager_".

    Borrowed from https://packaging.python.org/guides/creating-and-discovering-plugins/

    Big TODO: provide diagnostic info when importing or registration fails
    """
    for finder, name, ispkg in pkgutil.iter_modules():
        if (name.startswith("voyager_")):
            plugin: Type[Plugin] = importlib.import_module(name).Plugin
            if semver.satisfies(Plugins.INTERFACE_VERSION, plugin.required_plugin_version()):
                Plugins().register(plugin())
            else:
                print(f"Not loading plugin {plugin} - version mismatch "
                      + f"(required {plugin.required_plugin_version()}, actual {Plugins.INTERFACE_VERSION}")
