---
title: "Voyager"
---

## Introduction
Voyager is the package manager for SIATD and possibly Test Development

## Installation
### Windows
1. Download the latest version from [Artifactory](https://artifactory.prodrive.nl/artifactory/webapp/#/artifacts/browse/tree/General/siatd-generic-local/Tools/voyager)
    1. Please note that the onefile versions are meant for CI (They start slower)
2. Extract the zip file and place contents in `C:\voyager`
3. Add `C:\voyager` to the PATH variable
    1. Go to start and type `Edit environment variables for your account`
    2. In the User variables section select `Path` and click `Edit...`
    3. Add a `New` entry with the contents `C:\voyager`
    4. Click `Ok` and again `Ok` to save

## First time configuration
1. Open a command prompt and run `voyager config` to generate the default config file
2. The output of `voyager config` should indicate where to find the config file
3. Open the config file in a text editor
4. Get your Artifactory API key
    1. Go to your Artifactory `Edit Profile` page [link](https://artifactory.prodrive.nl/artifactory/webapp/#/profile)
    (click on your name on the top right side of the Artifactory webpage)
    2. Enter your password and press `Unlock`
    3. Generate and copy your API key
5. Fill in you API key in the between the empty quotes in the config file
6. Save the config file
7. Run `voyager config` again. It should print the contents of the config file

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
