import voyager.plugins
from voyager.voyager import cli

import click

def list_plugins():
    print("Loaded plugins:")
    for plugin in voyager.plugins.Plugins().plugins:
        print(f"  - {plugin}")

class VoyagerPlugin(voyager.plugins.Plugin):
    """A demo plugin for voyager that also tells you about the loaded plugins."""

    def __init__(self):
        super().__init__()
        # Register during plugin init - don't do *anything* without the plugin framework acting first
        cli.command("list-plugins")(list_plugins)

    def on_start(self):
        super().on_start()
