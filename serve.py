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
    def end_headers(self):
        # Prevent caching for development convenience
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

print(f"MIME type mapping configured (.mjs -> application/javascript)")
print(f"Starting server on: http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), MIMEHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
