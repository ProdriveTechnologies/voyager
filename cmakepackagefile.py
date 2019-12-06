from buildinfo import Package

class CMakePackageFile:
    def __init__(self, package: Package):
        self.package = package
        self.path = package.rootpath + 'CMakeLists.txt'

    def save(self):
        template = \
'''add_library({package_name} INTERFACE)

target_include_directories({package_name} INTERFACE
  {include_dirs}
)

target_link_libraries({package_name} INTERFACE
  {libs}
)
'''

        package_name = '{}-{}'.format(self.package.safe_name, self.package.version)
        include_dirs = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(dir) for dir in self.package.include_dirs]
        )
        libs = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(lib) for lib in self.package.libs]
        )

        text = template.format(
            package_name=package_name,
            include_dirs=include_dirs,
            libs=libs
        )

        with open(self.path, 'w') as cmake:
            cmake.write(text)
