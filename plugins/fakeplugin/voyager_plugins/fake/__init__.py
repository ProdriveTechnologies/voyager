import semver
from voyager import plugin_registry


class FakePlugin(plugin_registry.Plugin):
    REQUIRED_INTERFACE_VERSION = semver.Range("*", False)


# Finally, re-export the plugin class as "Plugin" so the plugin loader can find it.
Plugin = FakePlugin
