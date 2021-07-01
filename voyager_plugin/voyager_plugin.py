import click
import semver

from voyager import plugins


def list_plugins():
    print("Loaded plugins:")
    for plugin in plugins.Plugins().plugins:
        print(f"  - {plugin}")


class VoyagerPlugin(plugins.Plugin):
    """A demo plugin for voyager that also tells you about the loaded plugins."""

    REQUIRED_INTERFACE_VERSION = semver.Range("^0.1.0", False)

    def __init__(self):
        super().__init__()
        # Register during plugin init - don't do *anything* without the plugin framework acting first
        plugins.Plugins().add_command("list-plugins")(list_plugins)

    def on_start(self):
        super().on_start()
