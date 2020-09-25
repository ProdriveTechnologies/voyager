import json
import os
import shutil
import platform

from jsonschema import validate

from Singleton import SingletonType
from utilities import resource_path


class ConfigFile(metaclass=SingletonType):
    schema = {
        "type": "object",
        "properties": {
            "api_key": {"type" : "string"},
            "artifactory_url": {"type" : "string"},
            "default_arch": {"type" : "array", "items": {"type": "string"}}
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_dir = os.path.expanduser("~") + '/.voyager/'
        self._config_file = self._config_dir + 'config.json'
        self._api_key = ""
        self._artifactory_url = ""
        self._default_arch = []
        self._current_arch = []
        self._use_environ = os.environ.get('bamboo_voyager_CI')

    def exists(self) -> bool:
        if self._use_environ:
            return True
        else:
            return os.path.isfile(self._config_file)

    def parse(self) -> bool:
        if self._use_environ:
                self._api_key = os.environ.get('bamboo_voyager_CI_API_KEY').replace("\"", "")
                self._artifactory_url = os.environ.get('bamboo_voyager_CI_URL').replace("\"", "")
                archs = os.environ.get('bamboo_voyager_CI_ARCH').replace("\"", "")
                self._default_arch = archs.split(";")
                self._host_platform = self._default_arch
        else:
            with open(self._config_file) as json_file:
                data = json.load(json_file)
                validate(data, self.schema)
                self._api_key = data['api_key']
                self._artifactory_url = data['artifactory_url']
                self._default_arch = data['default_arch']
                self._host_platform = data['default_arch']
        
        if not self.api_key:
            return False
        
        return True

    def create_default(self):
        os.makedirs(self._config_dir, exist_ok=True)
        if platform.system() == 'Linux':
            location = resource_path('static/config_template_linux.json')
        else:
            location = resource_path('static/config_template_windows.json')
        shutil.copy(location, self._config_file)

    def update(self):
        json_data = {
            'api_key': self._api_key,
            'artifactory_url': self._artifactory_url,
            'default_arch': self._default_arch
        }
        with open(self._config_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    @property
    def artifactory_url(self):
        return self._artifactory_url

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
