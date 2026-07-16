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

import json
import os
import shutil
import platform

from jsonschema import validate

from .Singleton import SingletonType
from .utilities import resource_path

WINDOWS_CONFIG = {
    "token": "",
    "api_key": "",
    "artifactory_url": "",
    "default_arch": [
        "MSVC.143.DBG.32",
        "MSVC.142.DBG.32",
        "MSVC.141.DBG.32",
        "MSVC.140.DBG.32",
        "go.windows.amd64",
        "windows"
    ]
}

LINUX_CONFIG = {
    "token": "",
    "api_key": "",
    "artifactory_url": "",
    "default_arch": [
        "x86_64-linux-gnu-gcc-6",
        "go.linux.amd64"
    ]
}

class ConfigFile(metaclass=SingletonType):
    schema = {
        "type": "object",
        "properties": {
            "token": {"type" : "string"},
            "api_key": {"type" : "string"},
            "artifactory_url": {"type" : "string"},
            "default_arch": {"type" : "array", "items": {"type": "string"}}
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_dir = os.path.expanduser("~") + '/.voyager/'
        self._config_file = self._config_dir + 'config.json'
        self._token = ""
        self._api_key = ""
        self._artifactory_url = ""
        self._default_arch = []
        self._current_arch = []

    @property
    def _use_environ(self):
        # Setting this in __init__ breaks unit tests because ConfigFile is a singleton.
        return os.environ.get('bamboo_voyager_CI')

    def exists(self) -> bool:
        if self._use_environ:
            return True
        else:
            return os.path.isfile(self._config_file)

    def parse(self) -> bool:
        if self._use_environ:
                url, archs = require_env_vars(
                    [
                        "bamboo_voyager_CI_URL",
                        "bamboo_voyager_CI_ARCH",
                    ]
                )

                token = os.environ.get("bamboo_voyager_CI_TOKEN")
                api_key = os.environ.get("bamboo_voyager_CI_API_KEY")
                if token is None and api_key is None:
                    raise KeyError("Missing required environment variable(s): ['bamboo_voyager_CI_TOKEN', 'bamboo_voyager_CI_API_KEY']")

                self._token = token.replace("\"", "") if token else ""
                self._api_key = api_key.replace("\"", "") if api_key else ""
                self._artifactory_url = url.replace("\"", "")
                self._default_arch = archs.replace("\"", "").split(";")
                self._host_platform = self._default_arch
        else:
            with open(self._config_file) as json_file:
                data = json.load(json_file)
                validate(data, self.schema)
                self._token = data.get('token', "")
                self._api_key = data.get('api_key', "")
                self._artifactory_url = data['artifactory_url']
                self._default_arch = data['default_arch']
                self._host_platform = data['default_arch']
        
        return True

    def create_default(self):
        os.makedirs(self._config_dir, exist_ok=True)
        if platform.system() == 'Linux':
            with open(self._config_file, "w") as file:
                json.dump(LINUX_CONFIG, file, indent=2)
        else:
            with open(self._config_file, "w") as file:
                json.dump(WINDOWS_CONFIG, file, indent=2)

    def update(self):
        json_data = {
            'token': self._token,
            'api_key': self._api_key,
            'artifactory_url': self._artifactory_url,
            'default_arch': self._default_arch
        }
        with open(self._config_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    def get_primary_credential(self):
        if self._token:
            return ('token', self._token)
        if self._api_key:
            return ('api_key', self._api_key)
        return (None, None)

    def apply_auth_to_session(self, session):
        # Ensure a deterministic precedence: token first, then legacy API key.
        session.headers.pop('Authorization', None)
        session.headers.pop('X-JFrog-Art-Api', None)

        credential_type, credential_value = self.get_primary_credential()
        if credential_type == 'token':
            session.headers['Authorization'] = f'Bearer {credential_value}'
        elif credential_type == 'api_key':
            session.headers['X-JFrog-Art-Api'] = credential_value

        return session

    @staticmethod
    def check_for_valid_credentials():
        conf = ConfigFile()
        conf.parse()

        if not conf.token and not conf.api_key:
            raise ValueError("No Artifactory credentials found in ConfigFile. Please run 'voyager login' first")

    @property
    def artifactory_url(self):
        return self._artifactory_url

    @artifactory_url.setter
    def artifactory_url(self, url):
        self._artifactory_url = url

    @property
    def build_platform(self):
        return self._default_arch

    @property
    def host_platform(self):
        return self._host_platform

    @property
    def file_path(self):
        if self._use_environ:
            return "Overridden by environment variables"
        else:
            return self._config_file
    
    def set_host_platform(self, value):
        self._host_platform = [value]

    def set_host_platform_file(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            self._host_platform = data['host']


def require_env_vars(keys: list[str]) -> list[str]:
    values = []
    missing = []
    for key in keys:
        value = os.environ.get(key)
        if value is None:
            missing.append(key)
        else:
            values.append(value)

    if missing:
        raise KeyError(f"Missing required environment variable(s): {missing}")

    return values
