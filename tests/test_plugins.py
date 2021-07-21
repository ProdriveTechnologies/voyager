import sys
import unittest
import unittest.mock

import semver

import voyager.plugin_registry as registry
from voyager.configfile import ConfigFile

class TestPlugins(unittest.TestCase):
    def test_add_list(self):
        """When plugins are added, they show up in the plugin list"""
        under_test = registry.Registry()

        plugin1 = unittest.mock.Mock(spec=registry.Plugin)
        plugin2 = unittest.mock.Mock(spec=registry.Plugin)

        self.assertNotIn(plugin1, under_test.plugins)
        self.assertNotIn(plugin2, under_test.plugins)

        under_test.register(plugin1)
        self.assertIn(plugin1, under_test.plugins)
        self.assertNotIn(plugin2, under_test.plugins)

        under_test.register(plugin2)
        self.assertIn(plugin1, under_test.plugins)
        self.assertIn(plugin2, under_test.plugins)

    def test_load_plugins(self):
        under_test = registry.Registry()
        under_test.reset()

        registry.load_plugins()

        self.assertEqual(len(under_test.plugins), 1)
        self.assertEqual(type(under_test.plugins[0]).__name__, "PluginsPlugin")

    def test_find_versions_for_package(self):
        under_test = registry.Registry()
        ConfigFile().parse()
        voyager_versions = under_test.interface.find_versions_for_package(
            "siatd-generic-local", "Tools/voyager", ["win-setup"])
        self.assertTrue(any([semver.eq(x, "1.10.3", False) for x in voyager_versions]))
        self.assertTrue(any([semver.eq(x, "1.15.0", False) for x in voyager_versions]))

if __name__ == '__main__':
    unittest.main()
