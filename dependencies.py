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
        self.link = []
        
        self._find_link_file()

    @property
    def safe_name(self):
        return self._safe_name(self.name)
  
    def _safe_name(self, name:str):
        return name.replace("/", "-", -1)

    def _find_link_file(self):
        # When no link override from config file automagically discover lib files
        for x in self.lib_dirs:
            p = Path(self.rootpath + x)
            for f in p.glob('*.lib'): #TODO variable extension or **?
                self.link.append(f.name)

class BuildInfo:
    """Represents the build info. Contains multiple Packages"""
    def __init__(self, *args, **kwargs):
        self._packages = OrderedDict()

    def add_package(self, package:Package):
        self._packages[package.name] = package
        pass

    

class _Dependency:
    def __init__(self):
        self.rootpath = ""
        self.includedirs = []  # Ordered list of include paths
        self.libdirs = []  # Directories to find libraries
        self.bindirs = []  # Directories to find executables and shared libs
        # When package is editable, filter_empty=False, so empty dirs are maintained
        self.filter_empty = True

    def _filter_paths(self, paths):
        abs_paths = [os.path.join(self.rootpath, p)
                     if not os.path.isabs(p) else p for p in paths]
        if self.filter_empty:
            return [p for p in abs_paths if os.path.isdir(p)]
        else:
            return abs_paths

    @property
    def include_paths(self):
        return self._filter_paths(self.includedirs)

    @property
    def lib_paths(self):
        return self._filter_paths(self.libdirs)

    @property
    def bin_paths(self):
        return self._filter_paths(self.bindirs)

class Dependency(_Dependency):
    def __init__(self, root_folder):
        super(Dependency, self).__init__()
        self.rootpath = root_folder
        self.includedirs.append(DEFAULT_INCLUDE)
        self.libdirs.append(DEFAULT_LIB)
        self.bindirs.append(DEFAULT_BIN)

class Dependencies:
    def __init__(self):
        self._dependencies = OrderedDict()

    def _safe_name(self, name:str):
        return name.replace("/", "-", -1)

    @property
    def dependencies(self):
        return self._dependencies.items()

    @property
    def deps(self):
        return self._dependencies.keys()

    # Add functions to get all paths combined

    def update(self, name:str, inst:Dependency):
        self._dependencies[self._safe_name(name)] = inst