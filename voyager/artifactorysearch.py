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
            package_name = f"{split_uri[-5]}/{split_uri[-4]}"  # API/PA.Library
            repo = split_uri[-6]  # example-generic-local
            identifier = f"{repo}/{package_name}"
            if version not in found[identifier]:
                found[identifier].append(version)

    return found
