from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

latest_analysis = {
    "class": "Belum dianalisis",
    "confidence": 0
}

class AERIAHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/api/status":
            self.send_json({
                "app": "AERIA AI",
                "status": "online"
            })

        elif self.path == "/api/analysis":
            self.send_json(latest_analysis)

        else:
            super().do_GET()

    def do_POST(self):

        global latest_analysis

        if self.path == "/api/analysis":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            latest_analysis = {
                "class": data.get("class", "Unknown"),
                "confidence": data.get("confidence", 0)
            }

            self.send_json({
                "received": True,
                "result": latest_analysis
            })

        else:
            self.send_error(404)

    def send_json(self, data):
        response = json.dumps(data).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)


server = HTTPServer(("0.0.0.0", 5000), AERIAHandler)

print("AERIA AI WEBSITE AND API ONLINE!")
print("Open: http://localhost:5000")

server.serve_forever()
