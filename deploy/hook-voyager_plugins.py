# Because plugins are not directly imported, this module hook adds all modules
# found under the voyager_plugins namespace to the hidden imports.

from PyInstaller.utils.hooks import collect_submodules
hiddenimports = collect_submodules('voyager_plugins')
