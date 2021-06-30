import unittest
import unittest.mock

import voyager.plugins as plugins

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

if __name__ == '__main__':
    unittest.main()
