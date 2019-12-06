from buildinfo import Package

class CMakePackageFile:
  def __init__(self, package: Package):
    self.package = package

  def save(self):
    text = '''add_library({safe_name}-{version} INTERFACE)'''.format(
      safe_name = self.package.safe_name,
      version = self.package.version
    )

    with open(self.package.rootpath + 'CMakeLists.txt', 'w') as cmake:
      cmake.write(text)
