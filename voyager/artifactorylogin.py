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

from artifactory import ArtifactoryPath
import getpass
import click
import requests
from urllib.parse import urlparse

from .configfile import ConfigFile


def login():
    conf = ConfigFile()

    art_url_user = click.prompt("Please enter the Artifactory url", type=str)
    art_url = build_artifactory_url_from_user_input(art_url_user)

    user = getpass.getuser()
    user = click.prompt("User", default=user)
    pw = getpass.getpass(prompt=f"Password for {user}: ")

    click.confirm(f"Connecting as {user} to {art_url}. Continue?", abort=True)

    path = ArtifactoryPath(art_url, auth=(user, pw))
    token = _request_token(path, art_url, user)
    if token and _validate_token(token, art_url):
        print("Saving token to config file")
        conf.token = token
        conf.api_key = ""
        conf.artifactory_url = art_url
        conf.update()
        return

    raise ValueError("Could not get API Key from Artifactory, please generate it manually")


def _request_token(path, art_url: str, user: str) -> str:
    print("Requesting access token")
    token_url = f"{art_url}/api/security/token"
    payload = {
        "grant_type": "client_credentials",
        "username": user,
        "scope": "member-of-groups:*",
        "refreshable": True,
        "description": "voyager-generated"
    }

    try:
        response = path.session.post(token_url, data=payload)
        response.raise_for_status()
        content = response.json()
    except Exception:
        return ""

    return content.get("access_token", "")


def _validate_token(token: str, art_url: str) -> bool:
    validation_url = f"{art_url}/api/system/ping"
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"

    try:
        response = session.get(validation_url)
        response.raise_for_status()
        return True
    except Exception:
        return False


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
