"""WebUI for etptool

Author  : Jabez Winston <jabezwinston@gmail.com>
License : MIT
Date    : 18 December 2024
"""

import http.server
import socketserver

def main():
    PORT = 7080

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.path = "etptool/webui" + self.path    
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()

if __name__ == "__main__":
    main()