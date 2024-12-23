from http.server import SimpleHTTPRequestHandler, HTTPServer
def run_http_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_http_server(1234)