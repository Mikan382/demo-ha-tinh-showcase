#!/usr/bin/env python3
import http.server
import socketserver
import mimetypes
import sys

PORT = 8080
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

# Fix Windows MIME type issue for ES Modules (.mjs)
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('application/javascript', '.js')

class MIMEHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Windows registry may override mimetypes — force .mjs here
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.mjs': 'application/javascript'}

    def guess_type(self, path):
        if path.endswith('.mjs'):
            return 'application/javascript'
        return super().guess_type(path)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"MIME type mapping configured (.mjs -> application/javascript)")
print(f"Serving: {os.getcwd()}")
print(f"Starting server on: http://localhost:{PORT}")

with socketserver.ThreadingTCPServer(("", PORT), MIMEHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
