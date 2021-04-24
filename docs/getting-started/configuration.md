# Configuration
Voyager works together with Artifactory, connecting to an Artifactory instance can be done with the `voyager login` command.

1. Open a shell and run `voyager config` to generate the default config file
2. Run `voyager login` and follow the on screen instructions
3. Run `voyager config` again to view the contents of the config file

Example output:
```
Voyager version 1.15.0
Login and get Artifactory API key for config file
Please enter the artifactory url: https://artifactory.example.com/ui/packages
User [someuser]:
Password for someuser:
Connecting as someuser to https://artifactory.example.com/artifactory continue? [y/N]: y
Requesting API Key
Saving API key: .... to config file
```