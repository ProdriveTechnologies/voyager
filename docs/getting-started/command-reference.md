# Command reference
This chapter explains the commands that are available within voyager.

## Install
To use voyager for a project that already contains voyager.json files just run `voyager install` in the top level directory.
This should install all the dependencies. If you want to download the runtime transitive dependencies as well, run `voyager install --with-runtime-deps`
or shorter: `voyager install -wrd`.

## Search
You can search for packages by running `voyager search` with your query. A few example queries:

- `voyager search Interfaces/D*` Search for interfaces that start with a `D`
- `voyager search PA.*` Search for anything starting with PA.
- `voyager search P?.Bdm*` Search for Bdm in P?

Example output:
```
>voyager search PA.Jtag*
Voyager version 1.13.0
example-generic-local/API/PA.JtagProgrammer/19.0.2 ['18.0.0', '17.0.0', '19.0.0', '19.0.1', '19.0.2']
example-generic-local/API/PA.Jtag/13.0.0 ['13.0.0']
```
The first string of the search result can be copied and pasted in to the argument of the `voyager add` function.

## Add
You can add packages by running `voyager add` with a string of the package you want to add.
This package is then added in the voyager.json in the current working directory.
Example:
```
>voyager add example-generic-local/API/PA.JtagProgrammer/19.0.2
Voyager version 1.13.0
Adding Library:
  Repo:    example-generic-local
  Library: API/PA.JtagProgrammer
  Version: 19.0
``` 

## Deploy
To copy all the downloaded binaries (dll, so, exe) to a single directory `voyager deploy` can be used.
By default it will copy all the binaries to `.voyager/.deploy`, but the option `--dir` can be used to select a different directory.
For example to copy all binaries to the Debug folder use: `voyager deploy --dir Debug`.