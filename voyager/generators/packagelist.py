# Copyright 2022 Prodrive Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from voyager.generators.generator import Generator

from voyager.buildinfo import Package

class PackageListGenerator(Generator):
    FILE_TEMPLATE = """#pragma once

#include <string>
#include <map>

namespace Voyager
{{
const std::map<std::string, std::string> ArtifactVersions =
{{
  {0}
}};
}} // namespace Voyager
"""

    def _format_package_list(self):
        lines = list()
        for (name, package) in self.build_info.packages:
            package : Package = package
            lines.append(f'{{ "{name}", "{package.version}" }},')
        return self.FILE_TEMPLATE.format("\n  ".join(lines))

    @property
    def content(self):
        return self._format_package_list()
