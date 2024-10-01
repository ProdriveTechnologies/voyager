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

## Installation and usage
To use voyager, install one of the releases and run `voyager login` to authenticate with an Artifactory server.
After that run `voyager install` to install the dependencies of the project that you want to build.
For more information about the usage of voyager, take a look at the documentation site.

## Developing
Voyager is written in Python, 3.11 is the recommended version. To develop on the project create a virtual environment and run the python file.
```bash
 uv venv --python 3.11
 uv run voyager
```

## Contributing
See the [Contributing guidelines](CONTRIBUTING.md)

## Roadmap
- Investigate support for anonymous authentication
- Support for Artifactory Cloud. According to dohq-artifactory another [class](https://devopshq.github.io/artifactory/#artifactory-saas) needs to be used
- Add proper testcases that use Artifactory Cloud, so they are runnable  by everyone
- Change UpdateChecker class to read the latest version from Github releases

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)

## Contact
Feel free to open an issue with your questions or ideas.
If there's something that cannot be disclosed through an issue, for example, a vulnerability, then send an email to: opensource@prodrive-technologies.com
