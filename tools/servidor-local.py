"""Servidor local que comprime texto, como o Cloudflare Pages faz."""
import gzip, http.server, os, socketserver, sys

import pathlib
RAIZ = str(pathlib.Path(__file__).resolve().parent.parent)
COMPRIME = (".html", ".css", ".js", ".json", ".svg", ".xml", ".txt")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)
    def do_GET(self):
        caminho = self.translate_path(self.path)
        if os.path.isdir(caminho):
            caminho = os.path.join(caminho, "index.html")
        if not os.path.isfile(caminho):
            return super().do_GET()
        corpo = open(caminho, "rb").read()
        tipo = self.guess_type(caminho)
        cabecalhos = [("Content-Type", tipo), ("Cache-Control", "public, max-age=31536000")]
        if caminho.endswith(COMPRIME) and "gzip" in self.headers.get("Accept-Encoding", ""):
            corpo = gzip.compress(corpo, 6)
            cabecalhos.append(("Content-Encoding", "gzip"))
        self.send_response(200)
        for k, v in cabecalhos: self.send_header(k, v)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8900), Handler) as s:
    s.serve_forever()
