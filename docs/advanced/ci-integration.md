# CI Integration
Voyager needs to be configured with an Artifactory access token and information about which architectures to download.
This is done through a config file. This is not very practical when running in a CI setup.
To resolve this the config file is ignored when certain environment variables are set.

Use `bamboo_voyager_CI_TOKEN` as the default credential for CI.
`bamboo_voyager_CI_API_KEY` is still supported as a deprecated fallback for legacy pipelines.

## Environment variables
|Variable                  |Overrides       |Format|
|--------------------------|----------------|------|
|bamboo_voyager_CI         | -              |`true`|
|bamboo_voyager_CI_TOKEN   |access_token    |`"ACCESS_TOKEN_HERE"`|
|bamboo_voyager_CI_API_KEY |api_key (deprecated fallback) |`"API_KEY_HERE"`|
|bamboo_voyager_CI_URL     |artifactory_url |`"https://..."`|
|bamboo_voyager_CI_ARCH    |default_arch    |`"arch1;arch2;arch3"`|