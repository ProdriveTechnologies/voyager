import json, os, shutil

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
        self._use_environ = os.environ.get('voyager_CI')

    def exists(self) -> bool:
        if self._use_environ:
            return True
        else:
            return os.path.isfile(self._config_file)

    def parse(self) -> bool:
        if self._use_environ:
                self._api_key = os.environ.get('voyager_CI_API_KEY').replace("\"", "")
                self._artifactory_url = os.environ.get('voyager_CI_URL').replace("\"", "")
                archs = os.environ.get('voyager_CI_ARCH').replace("\"", "")
                self._default_arch = archs.split(";")
                self._current_arch = self._default_arch
        else:
            with open(self._config_file) as json_file:
                data = json.load(json_file)
                validate(data, self.schema)
                self._api_key = data['api_key']
                self._artifactory_url = data['artifactory_url']
                self._default_arch = data['default_arch']
                self._current_arch = data['default_arch']
        
        if not self.api_key:
            return False
        
        return True

    def create_default(self):
        os.makedirs(self._config_dir, exist_ok=True)
        location = resource_path('static/config_template.json')
        shutil.copy(location, self._config_file)

    @property
    def api_key(self):
        return self._api_key

    @property
    def artifactory_url(self):
        return self._artifactory_url

    @property
    def default_archs(self):
        return self._default_arch

    @property
    def current_archs(self):
        return self._current_arch

    @property
    def file_path(self):
        return self._config_file
