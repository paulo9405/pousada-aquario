"""
Troca o domínio de espaço reservado pelo definitivo, em todos os arquivos.

O sitemap e as tags Open Graph exigem URL absoluta — não dá para deixar
relativo como no canonical. Este script existe para que essa troca seja um
comando só, e não uma caçada por arquivo.

    python3 tools/definir-dominio.py https://pousadaaquarios.com.br

Rode antes de publicar. Sem isso, a prévia do link no WhatsApp não carrega a
imagem e o Google Search Console rejeita o sitemap.
"""
import glob, pathlib, re, sys

RESERVADO = "https://DOMINIO-A-DEFINIR"
RAIZ = pathlib.Path(__file__).resolve().parent.parent

def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    dominio = sys.argv[1].rstrip("/")
    if not re.match(r"^https?://[a-z0-9.-]+\.[a-z]{2,}$", dominio):
        print(f"domínio inválido: {dominio}"); sys.exit(1)

    alvos = (sorted(RAIZ.glob("*.html")) + [RAIZ / "sitemap.xml", RAIZ / "robots.txt"])
    total = 0
    for caminho in alvos:
        if not caminho.exists():
            continue
        texto = caminho.read_text(encoding="utf-8")
        n = texto.count(RESERVADO)
        if not n:
            continue
        caminho.write_text(texto.replace(RESERVADO, dominio), encoding="utf-8")
        total += n
        print(f"  {caminho.name}: {n} ocorrência(s)")

    print(f"\n{total} URLs atualizadas para {dominio}" if total
          else "\nnenhuma ocorrência encontrada — o domínio já foi definido?")

if __name__ == "__main__":
    main()
