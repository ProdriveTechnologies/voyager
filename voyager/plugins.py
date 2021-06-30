from .Singleton import SingletonType
from typing import List


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

    def on_start(self):
        for plugin in self.plugins:
            plugin.on_start()

    def on_end(self):
        for plugin in self.plugins:
            plugin.on_end()
