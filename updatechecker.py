
import threading
import semver
import click
from artifactdownloader import ArtifactDownloader

class UpdateChecker:
    def __init__(self):
        self._update_available = False
        self._new_version = None
        self._thread = None

    def check_for_update(self, current_version: str):
        down = ArtifactDownloader([], False, False)
        vers = down.find_versions_for_package("siatd-generic-local", "Tools/voyager", ["win-setup"])
        latest_version = semver.max_satisfying(vers, "*", True)
        if semver.lt(current_version, latest_version, False):
            self._update_available = True
            self._new_version = latest_version

    def check_for_update_in_background(self, current_version: str):
        # set daemon to true to Allow Python to immediately kill the thread on exit
        self._thread = threading.Thread(target=self.check_for_update, args=(current_version,), daemon=True)
        self._thread.start()

    def print_result(self):
        if self._thread is not None:
            self._thread.join()

        if self._update_available:
            click.echo(click.style(f"New version of voyager is available ({self._new_version}) please update",
                                   fg='yellow'))
