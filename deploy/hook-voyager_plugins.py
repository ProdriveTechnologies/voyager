# Because plugins are not directly imported, this module hook adds all modules
# found under the voyager_plugins namespace to the hidden imports.

from PyInstaller.utils.hooks import collect_submodules
import pkgutil
import voyager_plugins

hiddenimports = []

ns_pkg = voyager_plugins
prefix = ns_pkg.__name__ + "."
for p in pkgutil.iter_modules(ns_pkg.__path__, prefix):
    hiddenimports += collect_submodules(p[1])
