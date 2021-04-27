---
title: "Artifactory"
weight: 50
---

# Artifactory
Voyager packages are stored in [Artifactory](https://artifactory.prodrive.nl/artifactory/webapp/#/home)

## Layout
Voyager packages that are deployed must comply with the following path:
`[repository]/[group]/[package]/[version]/[arch]/`

|Element   |Description|
|----------|-----------|
|repository|The artifact repository, for example: `siatd-generic-local`|
|group     |Group folder in the repository: `API`, `ThirdParty`, ...|
|package   |Name of the package: `PA.Pig`, `fmt`, ...|
|version   |Version of the package, can be a semver number (x.y.z) or the name of a branch|
|arch      |The architecture of the packages, see [Architectures]({{< ref "#architectures" >}})|

## Architectures
The following architectures are known

|Key            |Description|
|---------------|-----------|
|**Windows**||
|MSVC.140.DBG.32|Visual Studio 2010 32bit Debug|
|MSVC.141.DBG.32|Visual Studio 2017 32bit Debug|
|MSVC.142.DBG.32|Visual Studio 2019 32bit Debug|
|go.windows.amd64|Golang 64 bit|
|windows|Generic Windows|
|**Linux**||
|arm-xilinx-eabi-gcc-4.8.1|Arm GCC 4.8.1 for Ets-Prg (Config 0)|
|arm-linux-gnueabi-gcc-7.2.1|Arm GCC 7.2.1 for Ets-Prg (Config 3)|
|x86_64-linux-gnu-gcc-6|GCC 6 for lnxdev|
|go.linux.amd64|Golang 64 bit|
|arm-marvell-linux-gnueabi-gcc-4.6.4|Arm GCC 4.6.4 for AET Bottom Backplane|
|**Any platform**||
|Header|Header-only packages|
|Source|Source packages|

## Properties
It is possible to add properties to an Artifact, these can be used to change the behavior of Voyager.
The following properties are supported:

|Name      |Description                                               |Value                                |
|----------|----------------------------------------------------------|-------------------------------------|
|deprecated|Indicate that the package is no longer recommended for use|Warning message to display in Voyager|