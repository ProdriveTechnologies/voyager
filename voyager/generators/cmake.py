# Copyright 2021 Prodrive Technologies
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
from pathlib import Path

class CMakeGenerator(Generator):
    subdir_template = 'add_subdirectory("{rootpath}")'

    def _format_subdirs(self):
        paths = [Path(package.rootpath) for _, package in self.build_info.packages]
        lines = [self.subdir_template.format(rootpath=path.as_posix()) for path in paths]
        return "\n".join(lines)

    @property
    def content(self):
        return self._format_subdirs()

class CMakeProjectGenerator(Generator):
    template = \
'''function(target_add_voyager target)
  {link_libraries}
endfunction()
'''
    link_libraries_template = 'target_link_libraries(${{target}} PUBLIC {package_name})'

    def _format_link_libraries(self):
        package_names = ['{}-{}'.format(p.safe_name, p.version) for _, p in self.build_info.packages]
        lines = [self.link_libraries_template.format(package_name=p) for p in package_names]
        return "\n  ".join(lines)

    @property
    def content(self):
        return self.template.format(
            link_libraries=self._format_link_libraries()
        )
