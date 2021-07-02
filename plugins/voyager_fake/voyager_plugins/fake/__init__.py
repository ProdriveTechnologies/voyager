import semver
from voyager import plugin_registry


class FakePlugin(plugin_registry.Plugin):
    REQUIRED_INTERFACE_VERSION = semver.Range("*", False)


Plugin = FakePlugin
