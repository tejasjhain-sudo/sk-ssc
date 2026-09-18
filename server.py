import http.server
import socketserver

import json
import os

PORT = 3000
DIRECTORY = "/Users/tejas/Desktop/website wquestio "

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/submit-test":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                submission = json.loads(post_data.decode("utf-8"))
                submissions_file = os.path.join(DIRECTORY, "test_submissions.json")
                data = []
                if os.path.exists(submissions_file):
                    try:
                        with open(submissions_file, "r") as f:
                            data = json.load(f)
                    except Exception:
                        data = []
                data.append(submission)
                with open(submissions_file, "w") as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Submission saved"}).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode("utf-8"))
                return
        return super().do_GET()

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Local server running at http://localhost:{PORT}")
        httpd.serve_forever()
