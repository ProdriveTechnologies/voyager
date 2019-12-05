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
|ARM.GCC.481|Arm GCC 4.8.1 for Ets-Prg (Config 0)|
|go.linux.amd64|Golang 64 bit|