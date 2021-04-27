# Voyager
Package manager for C/C++ software.

Voyager is an enterprise focused package manager for C and C++ that integrates with Artifactory:

- Integrates with Visual Studio (MSBuild) and CMake
- Host packages in your own network on your own server
- Works with the free Community Edition of Artifactory
- Easy to use, just call `voyager install` and then build your software the regular way
- Very simple package format, allowing easy packaging of existing software solutions (no need to overhaul your entire build system)

The reason we've created voyager at Prodrive Technologies is that third-party options did not fit our workflow.
We have a lot of existing software which would need significant changes to integrate with one of the existing package managers for C/C++.