from artifactory import ArtifactoryPath
from collections import defaultdict
import getpass

from configfile import ConfigFile


def login():
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}"
    api_key_url = f"{art_url}/api/security/apiKey"

    user = getpass.getuser()
    pw = getpass.getpass(prompt=f"Password for {user}: ")

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
