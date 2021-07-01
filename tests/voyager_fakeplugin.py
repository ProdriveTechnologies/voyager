import semver

import voyager.plugins


class FakePlugin(voyager.plugins.Plugin):
    # Claim compatibility with all Plugin.INTERFACE_VERSIONs
    REQUIRED_INTERFACE_VERSION = semver.Range("*", False)

# Export as "Plugin" so the plugin loader can find it.
Plugin = FakePlugin
