import sys
import unittest
import unittest.mock

import voyager.plugins as plugins


class TestPlugins(unittest.TestCase):
    def test_add_list(self):
        """When plugins are added, they show up in the plugin list"""
        under_test = plugins.Registry()

        plugin1 = unittest.mock.Mock(spec=plugins.Plugin)
        plugin2 = unittest.mock.Mock(spec=plugins.Plugin)

        self.assertNotIn(plugin1, under_test.plugins)
        self.assertNotIn(plugin2, under_test.plugins)

        under_test.register(plugin1)
        self.assertIn(plugin1, under_test.plugins)
        self.assertNotIn(plugin2, under_test.plugins)

        under_test.register(plugin2)
        self.assertIn(plugin1, under_test.plugins)
        self.assertIn(plugin2, under_test.plugins)

    def test_load_plugins(self):
        under_test = plugins.Registry()
        under_test.reset()

        sys.path = ["tests/plugins"] + sys.path
        plugins.load_plugins()
        sys.path = sys.path[1:]

        self.assertEqual(len(under_test.plugins), 2)  # one for voyager_plugin
        self.assertEqual(type(under_test.plugins[0]).__name__, "FakePlugin")


if __name__ == '__main__':
    unittest.main()
