# Cross compilation
To support cross-compilation, voyager distinguishes between the build
architecture and host architecture. The build architecture is that of the
system voyager and the compiler run on. The host architecture is that of the
system your build products will run on. This distinction is important when
fetching build tools from voyager - they should always be
packages for the build system.

For the configuration file, this means that the `build_tools`
dependencies are downloaded for the build architecture, while `libraries`
dependencies are downloaded for the host architecture.

The build architecture is defined by the `default_arch` field in the
configuration file or the environment variables. When not explicitly defined, the host architecture
defaults to the build architecture. The host architecture can be defined while
running `voyager install`:

```
$ voyager install --host ARM.GCC.481
$ voyager install --host-file Platforms/Windows-Platform.json
```

Windows-Platform.json:
```json
{
  "version": "1",
  "host": ["MSVC.142.DBG.32", "MSVC.141.DBG.32", "MSVC.140.DBG.32", "go.windows.amd64", "windows"]
}
```