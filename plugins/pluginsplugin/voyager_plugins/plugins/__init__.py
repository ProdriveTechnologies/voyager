# Sample voyager plugin that adds a "plugins" command to list the loaded plugins.
#
# A voyager plugin is a module that..
# - starts with "voyager_"
# - exports a type Plugin, which
# - implements voyager.plugins.Plugin
# It doesn't have to be a single file - a package will work just as well.

import click
import semver
from voyager import plugin_registry


class PluginsPlugin(plugin_registry.Plugin):
    """A demo plugin for voyager that also tells you about the loaded plugins."""

    REQUIRED_INTERFACE_VERSION = semver.Range("^0.1.0", False)

    def __init__(self, interface: plugin_registry.Interface):
        super().__init__(interface)
        # Register during plugin init - don't do *anything* without the plugin framework acting first
        self.interface.add_command("plugins")(self.list_plugins)

    def list_plugins(self):
        print("Loaded plugins:")
        for plugin in self.interface.plugins:
            print(f"  - {plugin}")

    def __str__(self):
        return f"{type(self).__name__} (module {__name__})"


# Finally, re-export the plugin class as "Plugin" so the plugin loader can find it.
Plugin = PluginsPlugin
