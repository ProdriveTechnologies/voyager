import unittest
import unittest.mock

import voyager.plugins as plugins
import sys

class TestPlugins(unittest.TestCase):
    def test_add_list(self):
        """When plugins are added, they show up in the plugin list"""
        underTest = plugins.Plugins()

        plugin1 = unittest.mock.Mock(spec=plugins.Plugin)
        plugin2 = unittest.mock.Mock(spec=plugins.Plugin)

        self.assertNotIn(plugin1, underTest.list())
        self.assertNotIn(plugin2, underTest.list())
      
        underTest.register(plugin1)
        self.assertIn(plugin1, underTest.list())
        self.assertNotIn(plugin2, underTest.list())

        underTest.register(plugin2)
        self.assertIn(plugin1, underTest.list())
        self.assertIn(plugin2, underTest.list())

    def test_load_plugins(self):
        underTest = plugins.Plugins()
        underTest.reset()

        sys.path = ["tests/plugins"] + sys.path
        plugins.load_plugins()
        sys.path = sys.path[1:]

        self.assertEqual(len(underTest.list()), 1)
        self.assertEqual(type(underTest.list()[0]).__name__, "FakePlugin")

if __name__ == '__main__':
    unittest.main()
