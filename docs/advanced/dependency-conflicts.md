# Dependency conflicts
This page explains how to use the `force_version` keyword to handle dependency conflicts.

## When
Conflicts occur when a voyager package requires a different version of an already included package.
For example: `Exceptions` requires `fmt` 6.2 and BitFields requires `fmt` 6.0. 
To reproduce this you can use the following json:
```json
[{
  "repo": "example-generic-local",
  "library": "Utils/Exceptions",
  "version": "1.2"
},
{
  "repo": "example-generic-local",
  "library": "Utils/BitFields",
  "version": "1.1"
}]
```
Which will result in the following error:
```
+-- Downloading Utils/Exceptions @ 1.2 ... MSVC.142.DBG.32 @ 1.2.0 OK
|   +- Downloading ThirdParty/fmt @ 6.2 ... MSVC.142.DBG.32 @ 6.2.0 OK
+-- Downloading Utils/BitFields @ 1.1 ... Header @ 1.1.0 OK
|   +- Downloading ThirdParty/fmt @ 6.0 ... ERROR: Version conflict within project for ThirdParty/fmt: 6.2.0 vs 6.0.0
```

## How to resolve
`force_version` can be used to force the usage of a specific version of a package.
To resolve conflicts in the above example change the voyager.json to this:
```json
[{
  "repo": "siatd-generic-local",
  "library": "ThirdParty/fmt",
  "version": "6.2",
  "force_version": true
},
{
  "repo": "siatd-generic-local",
  "library": "Utils/Exceptions",
  "version": "1.2"
},
{
  "repo": "siatd-generic-local",
  "library": "Utils/BitFields",
  "version": "1.1"
}]
```
Now fmt will be downloaded first and the force_version flag is saved. 
All other packages that require fmt will now be forced to use fmt 6.2
```
+-- Downloading ThirdParty/fmt @ 6.2 ... MSVC.142.DBG.32 @ 6.2.0 (Force Version) OK
+-- Downloading Utils/Exceptions @ 1.2 ... MSVC.142.DBG.32 @ 1.2.0 OK
|   +- Downloading ThirdParty/fmt @ 6.2 ... SKIP: package already included in project
+-- Downloading Utils/BitFields @ 1.1 ... Header @ 1.1.0 OK
|   +- Downloading ThirdParty/fmt @ 6.0 ... WARN: Forcing version 6.0.0 to 6.2.0 SKIP: package already included in project
```

## Rules
* You can only use force_version to force to a higher version. Otherwise an error is thrown: `ERROR: Cannot force 6.2.0 to lower version 6.0.0`
* You can always use force_version on non semver versions like branch names
* It is forbidden to have a force_version attribute in the voyager_package.json, it will be removed when `voyager package` is called
* Using force version can lead to unexpected behavior regarding ABI compatibility
* Libraries with force_version should be defined in the voyager.json before they're downloaded through a dependency