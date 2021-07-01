import click
import semver

from voyager import plugins


class VoyagerPlugin(plugins.Plugin):
    """A demo plugin for voyager that also tells you about the loaded plugins."""

    REQUIRED_INTERFACE_VERSION = semver.Range("^0.1.0", False)

    def __init__(self, interface: plugins.Interface):
        super().__init__(interface)
        # Register during plugin init - don't do *anything* without the plugin framework acting first
        self.interface.add_command("list-plugins")(self.list_plugins)

    def on_start(self):
        super().on_start()

    def list_plugins(self):
        print("Loaded plugins:")
        for plugin in self.interface.plugins:
            print(f"  - {plugin}")
