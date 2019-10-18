import os
from collections import OrderedDict
from pathlib import Path

DEFAULT_INCLUDE = "include"
DEFAULT_LIB = "lib"
DEFAULT_BIN = "bin"

class Package:
    """Represents a single voyager package"""
    def __init__(self, name, root_folder):
        self.name = name
        self.rootpath = root_folder
        self.include_dirs = [DEFAULT_INCLUDE]
        self.lib_dirs = [DEFAULT_LIB]
        self.bin_dirs = [DEFAULT_BIN]
        self.libs = []
        self.filter_empty = True
        
        self._find_link_file()

    @property
    def safe_name(self):
        return self._safe_name(self.name)
  
    @property
    def include_paths(self):
        return self._filter_paths(self.include_dirs)

    @property
    def lib_paths(self):
        return self._filter_paths(self.lib_dirs)

    @property
    def bin_paths(self):
        return self._filter_paths(self.bin_dirs)

    @property
    def lib_files(self):
        return self.libs

    def _filter_paths(self, paths):
        """This functions converts the internal package paths into full paths from the rootpath"""
        abs_paths = [os.path.join(self.rootpath, p)
                     if not os.path.isabs(p) else p for p in paths]
        if self.filter_empty:
            return [p for p in abs_paths if os.path.isdir(p)]
        else:
            return abs_paths

    def _safe_name(self, name:str):
        name = name.replace("/", "-", -1)
        name =  name.replace(".", "-", -1)
        return name

    def _find_link_file(self):
        # When no link override from config file automagically discover lib files
        for x in self.lib_dirs:
            p = Path(self.rootpath + x)
            for f in p.glob('*.lib'): #TODO variable extension or *.*
                self.libs.append(f.name)

class BuildInfo:
    """Represents the build info. Contains multiple Packages"""
    def __init__(self, *args, **kwargs):
        self._packages = OrderedDict()
        self.include_dirs = []
        self.lib_dirs = []
        self.bin_dirs = []
        self.libs = []

    def add_package(self, package:Package):
        self.include_dirs = self._merge_lists_without_duplicates(self.include_dirs, package.include_paths)
        self.lib_dirs = self._merge_lists_without_duplicates(self.lib_dirs, package.lib_paths)
        self.bin_dirs = self._merge_lists_without_duplicates(self.bin_dirs, package.bin_paths)
        self.libs = self._merge_lists_without_duplicates(self.libs, package.lib_files)
        self._packages[package.name] = package

    @property
    def packages(self):
        return self._packages.items()

    @property
    def package_names(self):
        return self._packages.keys()

    @property
    def include_paths(self):
        return self.include_dirs

    @property
    def lib_paths(self):
        return self.lib_dirs

    @property
    def bin_paths(self):
        return self.bin_dirs

    @property
    def lib_files(self):
        return self.libs

    def _merge_lists_without_duplicates(self, seq1, seq2):
        return [s for s in seq1 if s not in seq2] + seq2
