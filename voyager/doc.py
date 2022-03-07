# Copyright 2022 Prodrive Technologies
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

import http.server
import socketserver
import shutil

from voyager.lockfile import LockFileReader
from voyager.utilities import resource_path

ADDRESS = '127.0.0.1'
PORT = 1977


# https://stackoverflow.com/a/52531444
class DocHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='.voyager/', **kwargs)


def run_doc_server():
    # Check if lock file is available meaning that voyager install was executed
    reader = LockFileReader()
    reader.parse()

    # Copy html file from static to .voyager folder
    location = resource_path('static/voyager_doc_index.html')
    shutil.copy(location, '.voyager/index.html')

    # start a http server
    with socketserver.TCPServer((ADDRESS, PORT), DocHandler) as httpd:
        print(f"serving http server at http://{ADDRESS}:{PORT}")
        print("Press CTRL+C to stop")
        httpd.serve_forever()
