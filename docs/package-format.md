# Package format
This chapter explains the package format of a voyager package

## Layout
The standard layout of a voyager package looks like this. However this is fully modifiable through the voyager_package.json file.
The only thing that is mandatory in a package is the voyager_package.json.
```
voyager_package.tgz
|->voyager_package.json
|->Bin
   |->MyLibrary.dll
   |->MyLibrary.pdb
|->Include
   |->MyLibrary.h
|->Lib
   |->MyLibrary.lib
|->Doc
   |->Readme.html
```

## Compression
Packages are compressed using tar/gz, the extension is .tgz. To compress a package one can use the following Linux command:
`tar -czvf voyager_package.tgz Bin Doc Include Lib voyager_package.json`

## voyager_package.json

### Overview
This overview gives an idea of all the functionality in the package file. For a basic package only a few fields are needed.
```json
{
    "version": 2,
    "bin": ["Bin"],
    "include": ["Include"],
    "lib": ["Lib"],
    "link": ["PA.Library.R06.lib"],
    "definitions": [],
    "options": [{
        "key": "extended-header",
        "include": ["Include", "Include-Extended"]
    }],
    "dependencies": [
      {
        "repo": "example-generic-local",
        "library": "Interfaces/Standard",
        "version": "1.0",
        "options": [],
        "type": "compile"
      }
    ],
    "linker_flags": ["/DEF:${package_abs_path}Lib\\Client.def"]
}
```
#### Root elements
|Element     |Required|Description|
|------------|--------|-----------|
|version     |True    |The file format version, currently always 2|
|bin         |True*   |List of folders that contain the binaries  |
|include     |True*   |List of folders that contain the header files |
|lib         |True*   |List of folders that contain the lib files |
|link        |True*   |List of files to link to, files must be located in one of the `lib` directories|
|compile     |False   |List of files to compile.|
|definitions |True*   |Preprocessor definitions to set|
|options     |True*   |List of options that override other elements|
|dependencies|True*   |List of dependencies|
|linker_flags|False   |Additional linker flags, has support for template substitution|
\* Element is required but can be an empty array `[]` when not needed

#### Options elements
|Element    |Required|Description|
|-----------|--------|-----------|
|key        |True    |The key of the option, this is what the user provides in the `options` field in voyager.json|
|bin        |False   |Override the bin element|
|include    |False   |Override the include element|
|lib        |False   |Override the lib element|
|link       |False   |Override the link element|
|definitions|False   |Override the definitions element|

#### Dependencies elements
|Element |Required|Description|
|--------|--------|-----------|
|repo    |True    |The Artifactory repository in which the dependency is located|
|library |True    |The dependency to install|
|version |True    |Version to install, may contain wildcards like `3.*`|
|options |False   |dependency specific options|
|type    |False   |Dependency type for the package `compile` or `runtime`|

### Options
Options have the ability to override certain settings of the package. These options are completely package specific.
Example use cases for options include:

* Adding an extra include path for a 'secret' header (PA.Library.Extended.h)
* Modifying the link element to link to a static version of the library

### Template substitutions
Some fields have support for template substitutions, these can be used if an absolute path is needed in a specific command.
Available substitutions:

|Key                  |Substitution|
|---------------------|------------|
|`${package_abs_path}`|The full absolute path of the package folder ending with a /|