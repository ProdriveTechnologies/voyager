# Voyager.json
The voyager.json is the file that is placed in the solution and projects folder and lists all the dependencies.

## Overview
```json
{
  "version": 1,
  "type": "solution",
  "build_tools": [
    {
      "repo": "example-generic-local",
      "library": "Tools/TemplateSubstituter",
      "version": "3.*"
    },
    {
      "repo": "example-generic-local",
      "library": "Tools/cmake-toolchains",
      "version": "1",
      "output_dir": ".voyager/cmake-toolchains"
    },
    {
      "repo": "example-generic-local",
      "library": "Tools/cmake-utils",
      "version": "1",
      "output_dir": ".voyager/cmake-utils"
    }
  ],
  "libraries": [
    {
      "repo": "example-generic-local",
      "library": "API/ExampleLibrary",
      "version": "8.*",
    },
    {
      "repo": "example-generic-local",
      "library": "API/JtagProgrammer",
      "version": "6.0",
      "options": ["extended-header"],
      "dependency_type": "runtime",
      "for_archs": ["MSVC.142.DBG.32"],
      "force_version": true
    },
    {
      "repo": "example-generic-local",
      "library": "API/SwdProgrammer",
      "version": "*",
      "override_archs": ["arm-xilinx-eabi-gcc-4.8.1"],
      "download_only": true,
      "output_dir": ".voyager/SwdProgrammer"
    }
  ],
  "projects": ["Implementation", "Qualification"],
  "generators": ["msbuild", "cmake"]
}
```
### Root elements
|Element    |Required|Description|
|-----------|--------|-----------|
|version    |True    |The file format version, currently always 1|
|type       |True    |The type of the file: `solution` or `project`|
|build_tools|False   |List of packages to install that provide build tools.|
|libraries  |True    |List of packages to install that provide libraries, can be empty array `[]` for no packages|
|projects   |When `type:solution`|List of the subdirectories with voyager.json files where the type is `project`|
|generators |False   |At solution level: Which build systems to generate files for. Defaults to `["msbuild"]`.|

### Libraries & build tools elements
|Element         |Required|Description|
|----------------|--------|-----------|
|repo            |True    |The Artifactory repository in which the package is located|
|library         |True    |The package to install|
|version         |True    |Version to install, may contain wildcards like `3.*`|
|options         |False   |Package specific options, more about this in the [Package format](../package-format.md#options)|
|dependency_type |False   |Dependency type for the package `compile` or `runtime`, more about this in voyager_package.json|
|for_archs       |False   |Only install this package when installing for one of the architectures in this list|
|output_dir      |False   |Override the default output directory for the package. Can be useful if the build system has to make assumptions on the path|
|override_archs  |False   |Override the arch for a package, install the specified arch.|
|download_only   |False   |Only download this package, dont include the package and dont download dependencies.|
|force_version   |False   |Force this version when a dependency conflict occurs. See [Dependency Conflicts](../advanced/dependency-conflicts.md) for more information|
|local_path      |False   |Use a local package instead of downloading from Artifactory. Can be a relative or absolute path. Better to use this via the [Overlay file](../advanced/overlay-file.md)|

## Solution vs Project
The voyager.json has two types: `solution` and `project`. When a solution contains a single project a single voyager.json with the project type is enough.
A solution with multiple projects requires a voyager file for each project and a top level at the solution.

With a voyager solution, the solution file contains dependencies that are required for both projects. On top of that each project can have it's own dependencies.
```
MyProject
|->voyager.json (solution)
|->MyProject.sln
|->Implementation
   |->Implementation.vcxproj
   |->voyager.json (project)
   |->voyager.props (generated)
|->Qualification
   |->Qualification.vcxproj
   |->voyager.json (project)
   |->voyager.props (generated)
```

## Generators

Voyager supports multiple generators depending on what you're trying to build.
The default generator (if none are provided) is "msbuild".

|Name|Description|
|----|-----------|
|[msbuild](../integrations/msbuild.md)|Generates .props files to add to MSBuild projects.|
|[cmake](../integrations/cmake.md)|Generates .cmake files with INTERFACE libraries for each package for the CMake build system.|
|packagelist|Generates a `voyager.h` with a name &rarr; version map of all dependencies.|
