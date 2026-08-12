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
from datetime import datetime, timezone
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
    access_token, refresh_token = _request_token(path, art_url, user)
    if access_token:
        _validate_token(access_token, art_url)
        print("Saving token to config file")
        conf.access_token = access_token
        conf.refresh_token = refresh_token
        conf.token_created_timestamp = _current_timestamp_utc_iso8601()
        conf.api_key = ""
        conf.artifactory_url = art_url
        conf.update()
        return

    raise ValueError("Could not get API Key from Artifactory, please generate it manually")


def perform_token_refresh():
    conf = ConfigFile()

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {conf.access_token}"

    art_url = conf.artifactory_url
    jfrog_url = art_url.removesuffix("/artifactory")
    token_url = f"{jfrog_url}/access/api/v1/tokens"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": conf.refresh_token
    }

    try:
        response = session.post(token_url, data=payload)
        response.raise_for_status()
        content = response.json()
    except Exception as e:
        error_message = "Wrong login credentials" if "Bad credentials" in response.text else str(e)
        raise ValueError(f"Token request failed: {error_message}")

    access_token = content.get("access_token", "")
    if access_token:
        _validate_token(access_token, art_url)
        conf = ConfigFile()
        conf.access_token = access_token
        conf.refresh_token = content.get("refresh_token", "")
        conf.token_created_timestamp = _current_timestamp_utc_iso8601()
        conf.api_key = ""
        conf.artifactory_url = art_url
        conf.update()

def _request_token(path, art_url: str, user: str) -> tuple[str, str]:
    # jfrog_url is art_url but with the /artifactory path removed, because the token endpoint is not under /artifactory
    jfrog_url = art_url.removesuffix("/artifactory")

    print("Requesting access token")
    token_url = f"{jfrog_url}/access/api/v1/tokens"
    payload = {
        "grant_type": "client_credentials",
        "username": user,
        "scope": "applied-permissions/user",
        "refreshable": True,
        "description": "voyager-generated"
    }

    try:
        response = path.session.post(token_url, data=payload)
        response.raise_for_status()
        content = response.json()
    except Exception as e:
        error_message = "Wrong login credentials" if "Bad credentials" in response.text else str(e)
        raise ValueError(f"Token request failed: {error_message}")

    access_token = content.get("access_token", "")
    refresh_token = content.get("refresh_token", "")

    return (access_token, refresh_token)



def _validate_token(token: str, art_url: str):
    validation_url = f"{art_url}/api/system/ping"
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"

    try:
        response = session.get(validation_url)
        response.raise_for_status()
    except Exception as e:
        raise ValueError(f"Token validation failed: {e}")


def _current_timestamp_utc_iso8601() -> str:
    # Keep explicit UTC offset for reliable parsing across platforms.
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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
