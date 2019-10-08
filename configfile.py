import json, os
import click

from jsonschema import validate

from Singleton import SingletonType

class ConfigFile(metaclass=SingletonType):
    schema = {
        "type": "object",
        "properties": {
            "api_key": {"type" : "string"},
            "artifactory_url": {"type" : "string"},
            "default_arch": {"type" : "string"}
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_dir = os.path.expanduser("~") + '/.voyager/'
        self._config_file = self._config_dir + 'config.json'
        self._api_key = ""
        self._artifactory_url = ""
        self._default_arch = ""
        self._current_arch = ""

        if not os.path.isfile(self._config_file):
            self._create_default()
        
        self._parse()

    @property
    def api_key(self):
        return self._api_key

    @property
    def artifactory_url(self):
        return self._artifactory_url

    @property
    def default_arch(self):
        return self._default_arch

    @property
    def current_arch(self):
        return self._current_arch

    def _create_default(self):
        print()
        click.echo(click.style(f'It appears that there is no config file in {self.config_file}', fg='yellow'))
        click.echo("Generating a default one")
        os.makedirs(self._config_dir, exist_ok=True)
        data = {}
        data['api_key'] = ""
        data['artifactory_url'] = "https://artifactory.prodrive.nl/artifactory"
        data['default_arch'] = "MSVC.140.DBG.32"
        with open(self._config_file, 'w') as outfile:
            json.dump(data, outfile, indent=2)
        
        click.echo(click.style(u'Default one generated, please fill in you Artifactory API key', fg='red'))
        exit(1)

    def _parse(self):
        with open(self._config_file) as json_file:
            data = json.load(json_file)
            validate(data, self.schema)
            self._api_key = data['api_key']
            self._artifactory_url = data['artifactory_url']
            self._default_arch = data['default_arch']
            self._current_arch = data['default_arch']
