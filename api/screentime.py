from http.server import BaseHTTPRequestHandler
import json
import time
import os

DATA_FILE = "/tmp/screentime.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        if "/toggle/" in path:
            app = path.split("/toggle/")[-1]
            data = load_data()
            now = time.time()
            cutoff = now - 86400
            data = [d for d in data if d["time"] > cutoff]
            data.append({"app": app, "time": now})
            save_data(data)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        
        elif path == "/api/screentime" or path == "/api/screentime/":
            data = load_data()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        
        else:
            self.send_response(404)
            self.end_headers()