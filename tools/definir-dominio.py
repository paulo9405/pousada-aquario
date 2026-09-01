"""
Define (ou troca) o domínio do site em todos os arquivos que precisam de URL
absoluta.

O sitemap e as tags Open Graph exigem URL absoluta — não dá para deixar
relativo como seria possível no canonical. Este script existe para que essa
troca seja um comando só, e não uma caçada por arquivo.

    python3 tools/definir-dominio.py https://hotelpousadaquarios.paulodev.net

Funciona também para trocar um domínio já definido: ele descobre o atual
lendo o canonical do index.html, em vez de procurar só pelo espaço reservado.
Assim, corrigir um subdomínio digitado errado continua sendo um comando só.

Rode antes de publicar. Sem isso, a prévia do link no WhatsApp não carrega a
imagem e o Google Search Console rejeita o sitemap.
"""
import pathlib
import re
import sys

RESERVADO = "https://DOMINIO-A-DEFINIR"
RAIZ = pathlib.Path(__file__).resolve().parent.parent


def dominio_atual():
    """Lê o domínio em uso a partir do canonical da home."""
    index = (RAIZ / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<link rel="canonical" href="(https?://[^/"]+)', index)
    return m.group(1) if m else RESERVADO


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    novo = sys.argv[1].rstrip("/")
    if not re.match(r"^https?://[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9-]+)+$", novo):
        print(f"domínio inválido: {novo}")
        print("esperado algo como https://hotelpousadaquarios.paulodev.net")
        return 1

    atual = dominio_atual()
    if atual == novo:
        print(f"o domínio já é {novo} — nada a fazer")
        return 0

    print(f"trocando {atual} por {novo}\n")
    alvos = sorted(RAIZ.glob("*.html")) + [RAIZ / "sitemap.xml", RAIZ / "robots.txt"]
    total = 0
    for caminho in alvos:
        if not caminho.exists():
            continue
        texto = caminho.read_text(encoding="utf-8")
        n = texto.count(atual)
        if not n:
            continue
        caminho.write_text(texto.replace(atual, novo), encoding="utf-8")
        total += n
        print(f"  {caminho.name}: {n} ocorrência(s)")

    if total:
        print(f"\n{total} URLs atualizadas")
    else:
        print("\nnenhuma ocorrência encontrada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
