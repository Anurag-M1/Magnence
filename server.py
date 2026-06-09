import http.server
import socketserver
from pathlib import Path
from urllib.parse import unquote, urlparse

PORT = 8009

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    ROUTES = {
        "/": "index.html",
        "/blog": "blog.html",
        "/contact": "contact.html",
        "/services": "services.html",
        "/team": "team.html",
        "/work": "work.html",
    }

    def translate_path(self, path):
        parsed = urlparse(path)
        clean_path = unquote(parsed.path).rstrip("/") or "/"
        route = self.ROUTES.get(clean_path)

        if route is None and clean_path.startswith("/work/"):
            route = f"pages{clean_path}.html"
        elif route is None and clean_path.startswith("/blog/"):
            route = f"pages{clean_path}.html"
        elif route is None and "." not in Path(clean_path).name:
            route = clean_path.lstrip("/") + ".html"

        if route:
            candidate = Path.cwd() / route
            if candidate.is_file():
                return str(candidate)

        return super().translate_path(path)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == '__main__':
    # Allow immediate reuse of the port
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT} with caching disabled...")
        httpd.serve_forever()
