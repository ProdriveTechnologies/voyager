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
import subprocess
import sys
import webbrowser
import getpass
import click
import requests
from urllib.parse import urlparse

from .configfile import ConfigFile


def login():
    conf = ConfigFile()

    art_url_user = click.prompt("Please enter the Artifactory url", type=str)
    art_url = build_artifactory_url_from_user_input(art_url_user)

    token = _request_token_from_clipboard(art_url)
    if token and _validate_token(token, art_url):
        print("Saving token to config file")
        conf.token = token
        conf.api_key = ""
        conf.artifactory_url = art_url
        conf.update()
        return

    print("Could not request token. Falling back to API key flow")
    user = getpass.getuser()
    user = click.prompt("User", default=user)
    pw = getpass.getpass(prompt=f"Password for {user}: ")

    click.confirm(f"Connecting as {user} to {art_url}. Continue?", abort=True)

    path = ArtifactoryPath(art_url, auth=(user, pw))
    api_key = _request_api_key(path, art_url)
    if api_key:
        print(f"Saving API key: {api_key} to config file")
        conf.token = ""
        conf.api_key = api_key
        conf.artifactory_url = art_url
        conf.update()
        return

    raise ValueError("Could not get API Key from Artifactory, please generate it manually")


def _request_token_from_clipboard(art_url: str) -> str:
    user_profile_url = art_url.rstrip("artifactory") + "ui/user_profile"
    print(f"Opening browser: {user_profile_url}")
    webbrowser.open(user_profile_url)
    print("Generate an identity token in Artifactory and copy it to your clipboard.")
    token = click.prompt("Paste token or press Enter to read it from the clipboard", default="", show_default=False)
    if token:
        return token.strip()

    return _get_clipboard_text().strip()


def _get_clipboard_text() -> str:
    if sys.platform.startswith("win"):
        token = _run_clipboard_command(["powershell", "-NoProfile", "-Command", "Get-Clipboard"])
        if token:
            return token

    if sys.platform.startswith("linux"):
        for command in [
            ["xclip", "-selection", "clipboard", "-o"],
            ["xsel", "--clipboard", "--output"],
            ["wl-paste", "-n"],
        ]:
            token = _run_clipboard_command(command)
            if token:
                return token

    return ""


def _run_clipboard_command(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return ""


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


def _request_api_key(path, art_url):
    print("Requesting API Key")
    api_key_url = f"{art_url}/api/security/apiKey"

    try:
        response = path.session.get(api_key_url)
        response.raise_for_status()
        content = response.json()
    except Exception:
        content = {}

    api_key = content.get('apiKey', None)
    if not api_key:
        print("No API Key found in Artifactory, Generating one")
        try:
            response = path.session.post(api_key_url)
            response.raise_for_status()
            content = response.json()
            api_key = content.get('apiKey', None)
        except Exception:
            return ""

    return api_key or ""


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
