
import semver
from artifactdownloader import ArtifactDownloader

class UpdateChecker:
    def __init__(self):
        pass

    def check_for_update(self, current_version: str):
        down = ArtifactDownloader([], False)
        vers = down.find_versions_for_package("siatd-generic-local", "Tools/voyager", ["win-setup"])
        for ver in vers:
            if semver.lt(current_version, ver, False):
                print(f"New version out: {ver}")
                break
