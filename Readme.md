---
title: "Voyager"
bookCollapseSection: true
---

## Introduction
Voyager is the package manager for SIATD and possibly Test Development.

It is documented [on SiatDoc](https://artifactory.prodrive.nl/artifactory/siatd-generic-local/SiatDoc/docs/SIATD/Other/voyager/introduction.html).

## General usage
1. Run `voyager install` in the directory that contains the top level voyager.json file

## Contact information
If you have any feedback or request on this item, you can contact one of the following persons:

|Function|Name|
|--------|----|
|Owner   |Maarten Tamboer|
|Last Modified |<tag_last_commit_by>|

## Deploy folder
The deploy folder contains scripts to deploy voyager to the different platforms

## Release notes

### [1.6.0]
- Add support for linker_flags
- Fix bug for package names without a folder 
- Change the download folder from `libs` to `.voyager`

### [1.5.0]
- Add support for CMake to the `voyager install` command.
- Add a configuration option `generators` to the solution-level voyager file,
  to choose the desired project file generators.
- Add generator for -I parameters for header checks
- Add deprecation warnings through Artifactory properties
- Fix the exception when a branch name was available in Artifactory but the user used a semver

### [1.4.2]
- `voyager install` now touches the project files to force a Visual Studio reload

### [1.4.1]
- `voyager package` now accepts non-semver versions as dependencies (with a warning)

### [1.4.0]
- `voyager package` now expects an input file path and writes the output file in the same folder as the input file

### [1.3.0]
- Change environment variable names to the ones provided by the bamboo variables
- `voyager config` now prints the location of the config file
- Add support for preprocessor definitions

### [1.2.0]
- Add `voyager package` command

### [1.1.0]
- Add support for environment variables to override config file
- Multiple projects with a top level solution can be made
- Compatible architectures can now be defined in the config file
- Dependencies are automatically downloaded
- The version number can be indicated via semver ranges

### [1.0.0]
- First release of concept
