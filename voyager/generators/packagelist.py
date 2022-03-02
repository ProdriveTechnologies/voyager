from voyager.generators.generator import Generator

from voyager.buildinfo import Package

class PackageListGenerator(Generator):
    FILE_TEMPLATE = """#pragma once

#include <string>
#include <map>

namespace Voyager
{
const std::map<std::string, std::string> ArtifactVersions =
{
  {}
};
}
"""

    def _format_package_list(self):
        lines = list()
        for package in self.build_info.packages:
            package : Package = package
            lines += f'{{"{package.name}", "{package.version}" }},'
        return self.FILE_TEMPLATE.format("\n".join(lines))

    @property
    def content(self):
        return self._format_package_list()
