---
title: "Usage"
weight: 20
---
# Usage
This chapter explains how to use voyager for the installation of packages

## Basics
To use voyager for a project that already contains voyager.json files just run `voyager install` in the top level directory.
This should install all the dependencies.

## voyager.json
The voyager.json is the file that is placed in the solution and projects folder and lists all the dependencies.
### Overview
```json
{
  "version": 1,
  "type": "solution",
  "libraries": [
    {
      "repo": "siatd-generic-local",
      "library": "API/PA.Pig",
      "version": "6.0",
      "options": ["extended-header"],
      "dependency_type": "runtime"
    }
  ],
  "projects": ["Implementation", "Qualification"],
  "generators": ["msbuild", "cmake"]
}
```
#### Root elements
|Element   |Required|Description|
|----------|--------|-----------|
|version   |True    |The file format version, currently always 1|
|type      |True    |The type of the file: `solution` or `project`|
|libraries |True    |List of packages to install, can be empty array `[]` for no packages|
|projects  |When `type:solution`|List of the subdirectories with voyager.json files where the type is `project`|
|generators|False   |At solution level: Which build systems to generate files for. Defaults to `["msbuild"]`.|

#### Libraries elements
|Element         |Required|Description|
|----------------|--------|-----------|
|repo            |True    |The Artifactory repository in which the package is located|
|library         |True    |The package to install|
|version         |True    |Version to install, may contain wildcards like `3.*`|
|options         |False   |Package specific options, more about this in the [Package format]({{< ref "package_format.md#options" >}})|
|dependency_type |False   |Dependency type for the package `compile` or `runtime`, more about this in voyager_package.json|

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