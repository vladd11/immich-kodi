import http.client
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import xbmcaddon

DEBUG = False
if DEBUG:
    pass

HANDLE = xbmcaddon.Addon('plugin.video.immich')
RAW_SERVER_URL = HANDLE.getSetting("immich_url")
SERVER_URL = urlparse(RAW_SERVER_URL)
API_KEY = HANDLE.getSetting("api_key")


class MyHandler(BaseHTTPRequestHandler):
    def do(self, read, write=False):
        conn = http.client.HTTPSConnection(SERVER_URL.netloc) if SERVER_URL.scheme == 'https' \
            else http.client.HTTPConnection(SERVER_URL.netloc)
        post_data = None
        if write:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

        if self.headers['x-api-key'] != API_KEY:
            self.send_response(401)
            return

        url = urlparse(self.path)
        conn.request("GET" if read else "HEAD", url._replace(path=os.path.splitext(url.path)[0]).geturl(), post_data, self.headers)
        resp = conn.getresponse()

        self.send_response(200)
        for i in resp.headers:
            if i == 'ETag' or i == 'Connection' or i == 'Keep-Alive':
                continue
            self.send_header(i, resp.headers[i])
        self.end_headers()

        body = resp.read()
        if read:
            self.wfile.write(body)

    def do_HEAD(self):
        self.do(False)

    def do_GET(self):
        self.do(True)

    def do_POST(self):
        self.do(True, True)


server_address = ('', 6819)
httpd = HTTPServer(server_address, MyHandler)

httpd.serve_forever()

if DEBUG:
    import pydevd

    pydevd.stoptrace()
