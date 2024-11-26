# Release notes

### [1.17.1]
- Fix version number in installer

### [1.17.0]
- Add transitive tag to enable search within a remote repository.
- Add -C / --directory and -s / --select-result flags to `voyager add`.
- Publish a python wheel of voyager

### [1.16.5]
- Fix a bug where build tools in a subproject were never retrieved.

### [1.16.4]
- Use a persistent HTTP connection to make `voyager install` faster.

### [1.16.3]
- Preserve symlinks during `voyager deploy`.

### [1.16.2]
- Also deploy transitive runtime dependencies 

### [1.16.1]
- Change default install folder on Windows to `C:\Program Files\Prodrive\voyager`
- Add PATH variable now modifies the system PATH

### [1.16.0]
- `voyager login` now asks for the artifactory url and username
- Remove artifactory_url default value from config templates
- CMake and MSBuild generators now create a variable pointing to the `.voyager` directory.
- Add MSVC.143 to config_template Windows
- Implement plugin architecture
- Add generator for C++ header file with a list of installed packages
- Add missing docstrings so `voyager --help` is actually useful
- Add logging with the Python standard logging framework
- Add `voyager doc` command that hosts a local webserver linking to docs of packages
- Add `voyager check-update` command to find out which packages in voyager.json can be updated
- Add command line parameter to `voyager add` for force version
- Add command line parameter to `voyager deploy` to only deploy runtime dependencies
- Fix windows installer so updates can be installed without removing the old version first

### [1.15.0]
- Add `voyager login` so no more copying of API key is needed
- Fix bug where recursive runtime dependencies were not downloaded
- The generated default config file on Linux now contains the correct architectures
- When an update is available, the download link is printed

### [1.14.0]
- Add support for local packages through `local_path`
- Add option `--with-runtime-deps` for `voyager install` to also download runtime dependencies
- Add `voyager deploy` that copies the contents of all bin paths to an output folder

### [1.13.0]
- Add an update check that runs in the background of `voyager install`
- Add command to check for updates `voyager check-update`
- Add command to search for packages `voyager search`
- Add command to add found packages to voyager.json `voyager add`
- Fix bug where `output_dir` was placed in the package file

### [1.12.0]
- Add option `force_version` to handle version conflicts
- Fix issue with including dependencies of a skipped package
- Fix typo in missing config file message and make message stand out better

### [1.11.0]
- Add option `override_archs` for voyager.json to download a package that is a different arch then the host system.
- Add option `download_only` for downloading a package without including it.
- Update internal `_find_versions_for_package` function to use aql. Should give a good speed boost

### [1.10.3]
- Fixed a bug introduced in version 1.10.2 where package already included in another project would not be added to the build info and thus not included by the generators. 

### [1.10.2]
- Fixed bug where version conflicts would not occur between projects in a solution or between top-level dependencies and project-level dependencies. This now correctly throws an `ERROR: Version conflict`

### [1.10.1]
- Added installer

### [1.10.0]
- Add support for source packages.

### [1.9.0]
- Add support for output_dir to specify extraction directory per library

### [1.8.0]
- Add `for_archs` field in voyager.json to install package only for specific archs

### [1.7.1]
- Fixed bug `NameError: name 'build_tools' is not defined`

### [1.7.0]
- Add support for cross compilation through build_tools and selectable host_platform
- `voyager install` has now two optional commands: `--host` and `--host-file`
- Add support for `build_tools` element in voyager.json

### [1.6.1]
- Fix bug where project files were not getting touched

### [1.6.0]
- Add support for linker_flags
- Fix bug for package names without a folder
- Change the download folder from `libs` to `.voyager`

### [1.5.0]
- Add support for CMake to the `voyager install` command.
- Add a configuration option `generators` to the solution-level voyager file,
  to choose the desired project file generators.
- Add generator for -I parameters for header checks
- Add deprecation warnings through Artifactory properties
- Fix the exception when a branch name was available in Artifactory but the user used a semver

### [1.4.2]
- `voyager install` now touches the project files to force a Visual Studio reload

### [1.4.1]
- `voyager package` now accepts non-semver versions as dependencies (with a warning)

### [1.4.0]
- `voyager package` now expects an input file path and writes the output file in the same folder as the input file

### [1.3.0]
- Change environment variable names to the ones provided by the bamboo variables
- `voyager config` now prints the location of the config file
- Add support for preprocessor definitions

### [1.2.0]
- Add `voyager package` command

### [1.1.0]
- Add support for environment variables to override config file
- Multiple projects with a top level solution can be made
- Compatible architectures can now be defined in the config file
- Dependencies are automatically downloaded
- The version number can be indicated via semver ranges

### [1.0.0]
- First release of concept
