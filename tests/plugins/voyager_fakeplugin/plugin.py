import voyager.plugins

import semver

class FakePlugin(voyager.plugins.Plugin):
  # Claim compatibility with all Plugin.INTERFACE_VERSIONs
  REQUIRED_INTERFACE_VERSION = semver.Range("*", False)
