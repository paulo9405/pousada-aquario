"""
Servidor local que imita o Cloudflare Pages.

Reproduz três comportamentos que mudam o resultado dos testes:

1. **Compressão de texto.** O `python3 -m http.server` não comprime, e isso
   derruba a nota do Lighthouse artificialmente.
2. **URLs sem extensão.** O Pages serve `/contato` e redireciona
   `/contato.html` para lá com 308. Testar contra um servidor que entrega
   `.html` direto esconde redirecionamento em link interno, canonical e
   sitemap — foi o que aconteceu no primeiro deploy.
3. **404 de verdade.** Sem `404.html`, o Pages devolve 200 com a home em
   qualquer caminho inexistente.

    python3 tools/servidor-local.py
    # http://127.0.0.1:8900
"""
import gzip
import http.server
import os
import pathlib
import socketserver

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PORTA = 8900
COMPRIME = (".html", ".css", ".js", ".json", ".svg", ".xml", ".txt")
OCULTOS = ("_headers", "_redirects")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(RAIZ), **kw)

    def do_GET(self):
        caminho = self.path.split("?")[0].split("#")[0]

        # /contato.html -> 308 -> /contato, como o Pages faz
        if caminho.endswith(".html"):
            destino = "/" if caminho == "/index.html" else caminho[: -len(".html")]
            self.send_response(308)
            self.send_header("Location", destino)
            self.end_headers()
            return

        arquivo = self._resolver(caminho)
        if arquivo is None:
            return self._enviar(RAIZ / "404.html", status=404)
        return self._enviar(arquivo)

    def _resolver(self, caminho):
        rel = caminho.lstrip("/")
        if not rel:
            return RAIZ / "index.html"
        if any(rel.startswith(o) for o in OCULTOS):
            return None
        alvo = (RAIZ / rel).resolve()
        if RAIZ not in alvo.parents and alvo != RAIZ:
            return None
        if alvo.is_file():
            return alvo
        # /contato -> contato.html
        com_html = alvo.with_suffix(".html")
        if com_html.is_file():
            return com_html
        return None

    def _enviar(self, arquivo, status=200):
        if not arquivo or not arquivo.is_file():
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"404")
            return
        corpo = arquivo.read_bytes()
        cabecalhos = [("Content-Type", self.guess_type(str(arquivo)))]
        if arquivo.suffix in COMPRIME and "gzip" in self.headers.get("Accept-Encoding", ""):
            corpo = gzip.compress(corpo, 6)
            cabecalhos.append(("Content-Encoding", "gzip"))
        cabecalhos.append(("Cache-Control", "public, max-age=31536000"))
        self.send_response(status)
        for k, v in cabecalhos:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *a):
        pass


class Servidor(socketserver.ThreadingTCPServer):
    """Uma thread por conexão.

    Com o TCPServer de uma thread só, uma conexão presa bloqueia todas as
    outras — e o tools/qa.py, que abre dezenas de páginas em sequência nos
    dois navegadores, estourava o timeout no meio da varredura.
    """

    allow_reuse_address = True
    daemon_threads = True


def main():
    os.chdir(RAIZ)
    with Servidor(("127.0.0.1", PORTA), Handler) as s:
        print(f"servindo {RAIZ} em http://127.0.0.1:{PORTA}")
        s.serve_forever()


if __name__ == "__main__":
    main()
