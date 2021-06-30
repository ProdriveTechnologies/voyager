import voyager.plugins

class FakePlugin(voyager.plugins.Plugin):
  pass

voyager.plugins.Plugins().register(FakePlugin())
