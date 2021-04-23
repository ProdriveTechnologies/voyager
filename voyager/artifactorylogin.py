from artifactory import ArtifactoryPath
from collections import defaultdict
import getpass
import click
from urllib.parse import urlparse

from .configfile import ConfigFile


def login():
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}"
    api_key_url = f"{art_url}/api/security/apiKey"

    art_url_user = click.prompt("Please enter the Artifactory url", type=str)
    art_url = build_artifactory_url_from_user_input(art_url_user)

    user = getpass.getuser()
    user = click.prompt(f"User", default=user)
    pw = getpass.getpass(prompt=f"Password for {user}: ")

    click.confirm(f"Connecting as {user} to {art_url}. Continue?", abort=True)

    path = ArtifactoryPath(art_url, auth=(user, pw))
    print("Requesting API Key")
    r = path.session.get(api_key_url)
    r.raise_for_status()
    content = r.json()

    api_key = content.get('apiKey', None)
    if not api_key:
        print("No API Key found in Artifactory, Generating one")
        r = path.session.post(api_key_url)
        r.raise_for_status()
        content = r.json()
        api_key = content.get('apiKey', None)

    if not api_key:
        raise ValueError("Could not get API Key from Artifactory, please generate it manually")

    print(f"Saving API key: {api_key} to config file")

    conf.api_key = api_key

    conf.update()


def build_artifactory_url_from_user_input(art_url_user):
    # Depending on what the user puts in the prompt there are multiple paths to take
    # Something like: https://artifactory.example.com/ui/packages will yield
    # ParseResult(scheme='https', netloc='artifactory.example.com', path='/ui/packages', params='', query='', fragment='')
    # But artifactory.example.com will yield
    # ParseResult(scheme='', netloc='', path='artifactory.example.com', params='', query='', fragment='')
    art_url_parse = urlparse(art_url_user)
    if not art_url_parse.netloc:  # netloc is empty
        return f"https://{art_url_parse.path}/artifactory"

    return f"{art_url_parse.scheme}://{art_url_parse.netloc}/artifactory"
