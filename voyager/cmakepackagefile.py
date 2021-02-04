from buildinfo import Package

class CMakePackageFile:
    def __init__(self, package: Package):
        self.package = package
        self.path = package.rootpath + 'CMakeLists.txt'

    def save(self):
        template = \
'''cmake_minimum_required(VERSION 3.13)
add_library({package_name} INTERFACE)

target_include_directories({package_name} INTERFACE
  {include_dirs}
)

target_link_directories({package_name} INTERFACE
  {lib_dirs}
)

target_link_libraries({package_name} INTERFACE
  {libs}
)

target_sources({package_name} INTERFACE
  {sources}
)

target_compile_definitions({package_name} INTERFACE
  {defines}
)

target_link_options({package_name} INTERFACE
  {linker_flags}
)

list(APPEND CMAKE_PROGRAM_PATH
  {bins}
)
set(CMAKE_PROGRAM_PATH ${{CMAKE_PROGRAM_PATH}} PARENT_SCOPE)
'''

        package_name = '{}-{}'.format(self.package.safe_name, self.package.version)
        include_dirs = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(dir) for dir in self.package.include_dirs]
        )
        lib_dirs = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(dir) for dir in self.package.lib_dirs]
        )
        libs = '\n  '.join(
            ['"{}"'.format(lib) for lib in self.package.libs]
        )
        sources = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(src) for src in self.package.sources]
        )
        defines = '\n  '.join(self.package.defines)
        bins = '\n  '.join(
            ['"${{CMAKE_CURRENT_SOURCE_DIR}}/{}"'.format(dir) for dir in self.package.bin_dirs]
        )
        linker_flags = '\n  '.join(
            ['[=[{}]=]'.format(flag) for flag in self.package.linker_flags]
        )

        text = template.format(
            package_name=package_name,
            include_dirs=include_dirs,
            lib_dirs=lib_dirs,
            libs=libs,
            sources=sources,
            defines=defines,
            bins=bins,
            linker_flags=linker_flags
        )

        with open(self.path, 'w') as cmake:
            cmake.write(text)
