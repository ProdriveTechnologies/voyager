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

class HeaderCheckGenerator(Generator):
    template = '-I{include_dir}'

    def _format_include_dirs(self):
      include_paths = [Path(dir) for dir in self.build_info.include_dirs]
      include_paths = [self.template.format(include_dir=path.as_posix()) for path in include_paths]
      return ' '.join(include_paths)

    @property
    def content(self):
        return self._format_include_dirs()
