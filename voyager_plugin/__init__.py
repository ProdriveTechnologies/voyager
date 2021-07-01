# Re-export the plugin implementation with name "Plugin", so the loader can find it.
from .plugin import VoyagerPlugin as Plugin

# This sample plugin has a package + submodule, with plugin.py containing the
# actual plugin implementation. A single importable module (so for example
# voyager_plugin.py at the top level) should work just as well. So long as the
# python module named voyager_* exports a Plugin type, the plugin infrastructure
# can find it.
