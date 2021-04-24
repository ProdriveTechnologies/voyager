# Artifactory
Voyager packages are stored in [Artifactory](https://www.jfrog.com/)

## Layout
Voyager packages that are deployed must comply with the following path:
`[repository]/[group]/[package]/[version]/[arch]/`

|Element   |Description|
|----------|-----------|
|repository|The artifact repository, for example: `example-generic-local`|
|group     |Group folder in the repository: `API`, `ThirdParty`, ...|
|package   |Name of the package: `PA.JtagProgrammer`, `fmt`, ...|
|version   |Version of the package, can be a semver number (x.y.z) or the name of a branch|
|arch      |The architecture of the packages, see [Architectures](#architectures)|

## Architectures
The architecture indicates which platform the package has been made for. These are strings that are completely up to the end user.
The table below provides some examples of architecture strings.

|Key            |Description|
|---------------|-----------|
|**Windows**||
|MSVC.140.DBG.32|Visual Studio 2010 32bit Debug|
|MSVC.141.DBG.32|Visual Studio 2017 32bit Debug|
|MSVC.142.DBG.32|Visual Studio 2019 32bit Debug|
|go.windows.amd64|Golang 64 bit|
|windows|Generic Windows|
|**Linux**||
|arm-xilinx-eabi-gcc-4.8.1|Arm GCC 4.8.1|
|arm-linux-gnueabi-gcc-7.2.1|Arm GCC 7.2.1|
|x86_64-linux-gnu-gcc-6|GCC 6|
|go.linux.amd64|Golang 64 bit|
|**Any platform**||
|Header|Header-only packages|
|Source|Source packages|

## Properties
It is possible to add properties to an Artifact, these can be used to change the behavior of Voyager.
The following properties are supported:

|Name      |Description                                               |Value                                |
|----------|----------------------------------------------------------|-------------------------------------|
|deprecated|Indicate that the package is no longer recommended for use|Warning message to display in Voyager|
