import click
import semver

from voyager.plugins import Plugin, Interface


class VoyagerPlugin(Plugin):
    """A demo plugin for voyager that also tells you about the loaded plugins."""

    REQUIRED_INTERFACE_VERSION = semver.Range("^0.1.0", False)

    def __init__(self, interface: Interface):
        super().__init__(interface)
        # Register during plugin init - don't do *anything* without the plugin framework acting first
        self.interface.add_command("plugins")(self.list_plugins)

    def list_plugins(self):
        print("Loaded plugins:")
        for plugin in self.interface.plugins:
            print(f"  - {plugin}")

    def __str__(self):
        return f"{type(self).__name__} (module {__name__})"
