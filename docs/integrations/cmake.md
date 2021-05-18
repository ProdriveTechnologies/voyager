# CMake

The CMake generator creates files to include in your own `CMakeLists.txt` to
load voyager dependencies. The generator requires CMake 3.13 or higher.

## Usage
`CMakeLists.txt`:
```cmake
project(Library)
include(voyager_solution.cmake)
```

`Qualification/CMakeLists.txt`:
```cmake
add_executable(Qualification)
include(voyager.cmake)
target_add_voyager(Qualification)
```

## Generated files

Voyager generates three sets of files to include packages in your CMake
project: package files, a solution file, and project dependency files.

### Package files
For each voyager package, a `CMakeLists.txt` is generated that defines a new
target with the package's components (libraries, headers, and so on) as its
dependencies. The name of this target includes the path to the package and its
version, for example `ThirdParty-fmt-6.0.0`.

### Solution file
In the top-level of your project (the "solution" level, in Visual Studio terms)
a single file `voyager_solution.cmake` is generated. This file adds all voyager
packages as CMake subdirectories, allowing other projects to refer to the
targets defined for each package. In your top-level `CMakeLists.txt`, add
`include(voyager.cmake)` before any other `add_subdirectory` commands to make
them available to your subprojects.

### Project dependency files
In each of your sub-projects, a file `voyager.cmake` is generated. This module
defines a function `target_add_voyager(<target>)`, which adds all dependencies
for that subproject to the specified target. Include `voyager.cmake` and call
that function on your target, and you're good to go.
