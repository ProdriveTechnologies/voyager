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
from typing import Optional

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./voyager")

    return os.path.join(base_path, relative_path)

def solution_dot_voyager_path() -> Optional[str]:
    """ Get absolute path to the .voyager folder located in the solution directory """
    search_dir_name = ".voyager"
    current_dir = os.getcwd()

    # Check if directory exists in current location
    if os.path.isdir(os.path.join(current_dir, search_dir_name)):
        return os.path.join(current_dir, search_dir_name)
    # If not, check one directory up
    elif os.path.isdir(os.path.join(os.path.dirname(current_dir), search_dir_name)):
        return os.path.join(os.path.dirname(current_dir), search_dir_name)
    else:
        return None

