# Overlay file
The overlay file is made to override and add elements to a voyager.json file without modifying that file.
The overlay file should only exist locally on the machine of the developer. Don't commit it in git.

## Example use case
When developing a new package it might be useful to test if the package is working.
Therefore you might want to reference it locally without using Artifactory. This is possible by using an overlay file with a `local_path` element.

voyager.json
```json
{
  "version": 1,
  "type": "solution",
  "build_tools": [
  ],
  "libraries": [
    {
      "repo": "siatd-generic-local",
      "library": "WowALocalPackage",
      "version": "500.0.0"
    }
  ],
  "projects": ["Implementation"],
  "generators": ["msbuild"]
}
```

voyager.overlay.json
```json
{
  "version": 1,
  "type": "overlay",
  "build_tools": [],
  "libraries": [
    {
      "repo": "siatd-generic-local",
      "library": "WowALocalPackage",
      "local_path": "..\\WowALocalPackage\\Debug\\voyager_package"
    }
  ]
}
```

voyager install output
```
Overlay file active
Top level:
+-- Downloading WowALocalPackage @ 500.0.0 ... Overlay Local OK
|   +- Downloading Interfaces/Report @ 2.0 ... Header @ 2.0.0 OK
|   +- Downloading Interfaces/Jtag @ 1.0 ... Header @ 1.0.0 OK
```