from .Singleton import SingletonType
from pathlib import Path
from typing import List

import importlib
import pkgutil

class Plugin:
    def on_start(self):
        pass

    def on_end(self):
        pass


class Plugins(metaclass=SingletonType):
    def __init__(self):
        super().__init__()
        self.plugins: List[Plugin] = []

    def register(self, plugin: Plugin):
        self.plugins.append(plugin)

    def list(self) -> List[Plugin]:
        return list(self.plugins)

    def reset(self):
        """Reset the plugin registry. Only for test usage."""
        self.plugins = []

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
    """
    for finder, name, ispkg in pkgutil.iter_modules():
        if (name.startswith("voyager_")):
            importlib.import_module(name)
