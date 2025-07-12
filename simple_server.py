#!/usr/bin/env python3
"""
Simple HTTP server for testing AI Hedge Fund interface
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/test.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir('/workspace')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Simple HTTP Server running at:")
        print(f"   - http://127.0.0.1:{PORT}/")
        print(f"   - http://172.30.0.2:{PORT}/")
        print(f"📄 Serving test.html from /workspace")
        print(f"Press Ctrl+C to stop")
        print("")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
            httpd.shutdown()