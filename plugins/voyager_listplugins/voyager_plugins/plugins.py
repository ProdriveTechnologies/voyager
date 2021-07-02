# Copyright 2021 Prodrive Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Sample voyager plugin that adds a "plugins" command to list the loaded plugins.
#
# A voyager plugin is a pip-installable module that..
# - is part of the namespace package "voyager_plugins"
# - exports a type Plugin, which
# - implements voyager.plugin_registry.Plugin

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

# And export the plugin class with name "Plugin" so the loader can find it.
Plugin = PluginsPlugin
