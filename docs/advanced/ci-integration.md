# CI Integration
Voyager needs to be configured with an API Key for Artifactory and information about which architectures to download.
This is done through a config file. This is not very practical when running in a CI setup.
To resolve this the config file is ignored when certain environment variables are set.

## Environment variables
|Variable                  |Overrides       |Format|
|--------------------------|----------------|------|
|bamboo_voyager_CI         | -              |`true`|
|bamboo_voyager_CI_API_KEY |api_key         |`"API_KEY_HERE"`|
|bamboo_voyager_CI_URL     |artifactory_url |`"https://..."`|
|bamboo_voyager_CI_ARCH    |default_arch    |`"arch1;arch2;arch3"`|