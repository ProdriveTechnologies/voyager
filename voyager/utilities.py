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

import sys
import os
import hashlib
from pathlib import Path
from typing import Optional

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./voyager")

    return os.path.join(base_path, relative_path)

def md5hash(filename):
    h = hashlib.md5()
    with open(filename,'rb') as f: 
        while True:
            data = f.read(8192)
            if not data:
                break
            h.update(data)
    return h.hexdigest()

def solution_dot_voyager_path() -> Optional[str]:
    """ Get absolute path to the .voyager folder located in the solution directory 
    
    Will only search in the current directory or one directory up
    """
    search_dir_name = ".voyager"
    current_dir = Path.cwd()

    if (current_dir / search_dir_name).is_dir():
        return current_dir / search_dir_name
    elif (current_dir.parents[0] / search_dir_name).is_dir():
        return current_dir.parents[0] / search_dir_name
    else:
        return None

