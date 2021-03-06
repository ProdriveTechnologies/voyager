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
from collections import defaultdict

from .configfile import ConfigFile


def gavc(group_id=None, artifact_id=None, version=None, classifier=None, repos=None):
    conf = ConfigFile()
    art_url = f"{conf.artifactory_url}"
    gavc_url = f"{art_url}/api/search/gavc"
    payload = {}  # [g=groupId][&a=artifactId][&v=version][&c=classifier][&repos=x[,y]]
    if group_id:
        payload['g'] = group_id
    if artifact_id:
        payload['a'] = artifact_id
    if version:
        payload['v'] = version
    if classifier:
        payload['c'] = classifier
    if repos:
        payload['repos'] = ','.join(repos)

    path = ArtifactoryPath(art_url, apikey=conf.api_key)
    r = path.session.get(gavc_url, params=payload)
    r.raise_for_status()
    content = r.json()

    found = defaultdict(list)
    for result in content['results']:
        split_uri = result['uri'].split('/')
        if split_uri[-1] == "voyager_package.tgz":
            version = split_uri[-3] # 1.0.0
            package_name = f"{split_uri[-5]}/{split_uri[-4]}"  # API/Library
            repo = split_uri[-6]  # example-generic-local
            identifier = f"{repo}/{package_name}"
            if version not in found[identifier]:
                found[identifier].append(version)

    return found
