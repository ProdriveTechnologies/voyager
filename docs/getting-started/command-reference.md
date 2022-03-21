# Command reference
This chapter explains the commands that are available within voyager.

## Install
To use voyager for a project that already contains voyager.json files, run `voyager install` in the top level directory.
This should install all the dependencies. If you want to download the runtime transitive dependencies as well, run `voyager install --with-runtime-deps`
or shorter: `voyager install -wrd`.

## Search
You can search for packages by running `voyager search` with your query. A few example queries:

- `voyager search Interfaces/D*` Search for interfaces that start with a `D`
- `voyager search ASD.*` Search for anything starting with ASD.
- `voyager search P?.Xyz*` Search for Xyz in P?

Example output:
```
>voyager search Jtag*
Voyager version 1.13.0
example-generic-local/API/JtagProgrammer/19.0.2 ['18.0.0', '17.0.0', '19.0.0', '19.0.1', '19.0.2']
example-generic-local/API/Jtag/13.0.0 ['13.0.0']
```
The first string of the search result can be copied and pasted in to the argument of the `voyager add` function.

## Add
You can add packages by running `voyager add` with a string of the package you want to add.
This package is then added in the voyager.json in the current working directory.
The optional `--force-version` argument can be passed to add  `"force_version": "true"` to the json entry.  
Example:
```
>voyager add example-generic-local/API/JtagProgrammer/19.0.2
Voyager version 1.13.0
Adding Library:
  Repo:    example-generic-local
  Library: API/JtagProgrammer
  Version: 19.0
``` 

## Deploy
To copy all the downloaded binaries (dll, so, exe) to a single directory, `voyager deploy` can be used.
By default it will copy all the binaries to `.voyager/.deploy`, but the option `--dir` can be used to select a different directory.
The option `--only-runtime-deps` will limit the copy to only packages that are marked with the entry `"dependency_type": "runtime"`.  
For example to copy all binaries to the Debug folder, use `voyager deploy --dir Debug`.

## Check update
Find out which packages can be updated in the voyager.json.  
Example:
```
>voyager check-update
Voyager version 1.16.0
Patch Update Backwards-compatible bug fixes.
 Tools/FillTemplate                      3.2.2 -> 3.2.5      "version": "3.2"

Minor Update New backwards-compatible features.
 Utils/Exceptions                        1.1.2 -> 1.2.5      "version": "1.2"

Major Update Potentially breaking API changes, use caution.
 API/I2c                                 7.0.0 -> 8.0.0      "version": "8.0"
```

## Doc
Run `voyager doc` to start a local webserver that shows a listing of all the packages that contain a `Doc/Readme.html` file
