
from generators.generator import Generator
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
