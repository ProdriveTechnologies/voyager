---
title: "Config file"
weight: 30
---

# Config file
Voyager needs to be configured with an API Key for Artifactory and information about which architectures to download.
This is done through a config file. To find the file location and contents run `voyager config`.

## Location
The config file is located in the home folder

|Platform|Location|
|--------|--------|
|Windows |`%home%\.voyager\config.json`|
|Linux   |`$HOME/.voyager/config.json`|

## Format
```json
{
  "api_key": "API_KEY_HERE",
  "artifactory_url": "https://artifactory.prodrive.nl/artifactory",
  "default_arch": ["MSVC.142.DBG.32", "MSVC.141.DBG.32", "MSVC.140.DBG.32", "go.windows.amd64", "windows"]
}
```
#### Root elements
|Element         |Required|Description|
|----------------|--------|-----------|
|api_key         |True    |The Artifactory API key|
|artifactory_url |True    |Base URL of Artifactory|
|default_arch    |True    |List of architectures that are allowed to download. The order of these are the priority, so first a package with 142 is searched|

## Environment variables
A config file is not practical in CI environments. Therefore it is possible to override the config file through environment variables.

|Variable                  |Overrides       |Format|
|--------------------------|----------------|------|
|bamboo_voyager_CI         | -              |`true`|
|bamboo_voyager_CI_API_KEY |api_key         |`"API_KEY_HERE"`|
|bamboo_voyager_CI_URL     |artifactory_url |`"https://..."`|
|bamboo_voyager_CI_ARCH    |default_arch    |`"arch1;arch2;arch3"`|