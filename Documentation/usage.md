---
title: "Usage"
weight: 20
---
# Usage
This chapter explains how to use voyager for the installation of packages

## Basics
To use voyager for a project that already contains voyager.json files just run `voyager install` in the top level directory.
This should install all the dependencies.

## Search
You can search for packages by running `voyager search` with your query. A few example queries:

- `voyager search Interfaces/D*` Search for interfaces that start with a `D`
- `voyager search PA.*` Search for anything starting with PA
- `voyager search P?.Bdm*` Search for Bdm in PA and PI

Example output:
```
>voyager search PA.Jtag*
Voyager version 1.13.0
siatd-generic-local/API/PA.JtagProgrammer/19.0.2 ['18.0.0', '17.0.0', '19.0.0', '19.0.1', '19.0.2']
siatd-generic-local/API/PA.Jtag/13.0.0 ['13.0.0']
```
The first string of the search result can be copied and pasted in to the argument of the `voyager add` function.

## Add
You can add packages by running `voyager add` with a string of the package you want to add.
This package is then added in the voyager.json in the current working directory.
Example:
```
>voyager add siatd-generic-local/API/PA.JtagProgrammer/19.0.2
Voyager version 1.13.0
Adding Library:
  Repo:    siatd-generic-local
  Library: API/PA.JtagProgrammer
  Version: 19.0
``` 

## voyager.json
The voyager.json is the file that is placed in the solution and projects folder and lists all the dependencies.
### Overview
```json
{
  "version": 1,
  "type": "solution",
  "build_tools": [
    {
      "repo": "siatd-generic-local",
      "library": "Tools/FillTemplate",
      "version": "3.*"
    },
    {
      "repo": "siatd-generic-local",
      "library": "Tools/cmake-toolchains",
      "version": "1",
      "output_dir": ".voyager/cmake-toolchains"
    },
    {
      "repo": "siatd-generic-local",
      "library": "Tools/cmake-utils",
      "version": "1",
      "output_dir": ".voyager/cmake-utils"
    }
  ],
  "libraries": [
    {
      "repo": "siatd-generic-local",
      "library": "API/PA.Pig",
      "version": "6.0",
      "options": ["extended-header"],
      "dependency_type": "runtime",
      "for_archs": ["MSVC.142.DBG.32"],
      "force_version": true
    },
    {
      "repo": "siatd-generic-local",
      "library": "API/PA.SwdProgrammer",
      "version": "*",
      "override_archs": ["arm-xilinx-eabi-gcc-4.8.1"],
      "download_only": true,
      "output_dir": ".voyager/PA.SwdProgrammer"
    }
  ],
  "projects": ["Implementation", "Qualification"],
  "generators": ["msbuild", "cmake"]
}
```
#### Root elements
|Element    |Required|Description|
|-----------|--------|-----------|
|version    |True    |The file format version, currently always 1|
|type       |True    |The type of the file: `solution` or `project`|
|build_tools|False   |List of packages to install that provide build tools.|
|libraries  |True    |List of packages to install that provide libraries, can be empty array `[]` for no packages|
|projects   |When `type:solution`|List of the subdirectories with voyager.json files where the type is `project`|
|generators |False   |At solution level: Which build systems to generate files for. Defaults to `["msbuild"]`.|

#### Libraries & build tools elements
|Element         |Required|Description|
|----------------|--------|-----------|
|repo            |True    |The Artifactory repository in which the package is located|
|library         |True    |The package to install|
|version         |True    |Version to install, may contain wildcards like `3.*`|
|options         |False   |Package specific options, more about this in the [Package format]({{< ref "package_format.md#options" >}})|
|dependency_type |False   |Dependency type for the package `compile` or `runtime`, more about this in voyager_package.json|
|for_archs       |False   |Only install this package when installing for one of the architectures in this list|
|output_dir      |False   |Override the default output directory for the package. Can be useful if the build system has to make assumptions on the path|
|override_archs  |False   |Override the arch for a package, install the specified arch.|
|download_only   |False   |Only download this package, dont include the package and dont download dependencies.|
|force_version   |False   |Force this version when a dependency conflict occurs. See [Dependency Conflicts]({{< ref "conflicts.md" >}}) for more information|

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

## Build and host architectures
To support cross-compilation, voyager distinguishes between the build
architecture and host architecture. The build architecture is that of the
system voyager and the compiler run on. The host architecture is that of the
system your build products will run on. This distinction is important when
fetching build tools such as FillTemplate from voyager - they should always be
packages for the build system.

For the configuration file, this means that the `build_tools`
dependencies are downloaded for the build architecture, while `libraries`
dependencies are downloaded for the host architecture.

The build architecture is defined by the `default_arch` field in the
[configuration file]({{< ref "config_file.md" >}}) or the environment variables
defined in that section. When not explicitly defined, the host architecture
defaults to the build architecture. The host architecture can be defined while
running `voyager install`:

```
$ voyager install --host ARM.GCC.481
$ voyager install --host-file Platforms/Windows-Platform.json
```

Windows-Platform.json:
```json
{
  "version": "1",
  "host": ["MSVC.142.DBG.32", "MSVC.141.DBG.32", "MSVC.140.DBG.32", "go.windows.amd64", "windows"]
}
```
