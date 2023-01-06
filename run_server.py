import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint

PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the JSON payload of the request
        payload_len = int(self.headers.get("Content-Length"))
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload.decode("utf-8"))

        # Output the payload to the console
        pprint(payload)

        # Send a response with a 200 status code
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    print(f"start listening on port {PORT}")
    httpd = HTTPServer(("localhost", PORT), RequestHandler)
    httpd.serve_forever()
