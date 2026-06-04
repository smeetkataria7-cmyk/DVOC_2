"""Dev preview server for the DVOC site.

Why this exists instead of plain `python -m http.server`:
- Sends `Content-Type: text/html; charset=utf-8` so browsers never
  misdecode UTF-8 (emojis, dashes) as Windows-1252 -> mojibake.
- Sends `Cache-Control: no-store` so the browser never shows a stale
  page during development.
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 3000


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        ctype = super().guess_type(path)
        if ctype in ("text/html", "text/plain", "text/css", "application/javascript", "text/javascript"):
            return ctype + "; charset=utf-8"
        return ctype


if __name__ == "__main__":
    print(f"DVOC dev server running at http://localhost:{PORT} (UTF-8, no-cache)")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
