from .Singleton import SingletonType
from pathlib import Path
from typing import List

import importlib
import pkgutil

class Plugin:
    """
    Base for a voyager plugin.
    
    Plugins don't have to inherit from it, but all Plugin methods must be defined.
    """
    def on_start(self):
        pass

    def on_end(self):
        pass


class Plugins(metaclass=SingletonType):
    """
    Plugin manager.
    
    Plugin registration happens here, and you can poke the on_x methods to
    trigger event handlers in the registered plugins.
    """
    def __init__(self):
        super().__init__()
        self.plugins: List[Plugin] = []

    def register(self, plugin: Plugin):
        """
        Add a plugin to the registry.
        
        All registered plugins will be notified of events.
        """
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

    Big TODO: provide diagnostic info when importing or registration fails
    """
    for finder, name, ispkg in pkgutil.iter_modules():
        if (name.startswith("voyager_")):
            module = importlib.import_module(name)
            Plugins().register(module.Plugin())
