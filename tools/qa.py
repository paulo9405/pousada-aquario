"""
QA antes da publicação — checklist da seção 24 do roadmap.

Roda tudo que dá para automatizar: links, WhatsApp, mapa, menu, imagens,
metadados, dados estruturados e estrutura de cabeçalhos. Em Chromium e, se
estiver instalado, também em Firefox.

    python3 tools/servidor-local.py &
    python3 tools/qa.py

Saída: um relatório com [ok] e [FALHA] por item. Qualquer [FALHA] impede a
publicação.
"""
import json
import re
import sys
import urllib.error
import urllib.request

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8900"
PAGINAS = ["index.html", "acomodacoes.html", "pousada.html", "contato.html"]
LARGURAS = [320, 375, 390, 430, 768, 1024, 1280, 1440]

falhas = []
avisos = []


def checa(condicao, rotulo, detalhe=""):
    if condicao:
        print(f"  [ok]    {rotulo}")
    else:
        print(f"  [FALHA] {rotulo}{' — ' + detalhe if detalhe else ''}")
        falhas.append(rotulo)


def avisa(rotulo, detalhe=""):
    print(f"  [aviso] {rotulo}{' — ' + detalhe if detalhe else ''}")
    avisos.append(rotulo)


def links(pg):
    return pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")


def seccao(titulo):
    print(f"\n=== {titulo} ===")


def rodar(nav, nome_nav):
    seccao(f"Navegador: {nome_nav}")
    externos = set()

    for pagina in PAGINAS:
        pg = nav.new_page(viewport={"width": 1280, "height": 900})
        erros_console, falhas_rede = [], []
        pg.on("console", lambda m: erros_console.append(m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: falhas_rede.append(r.url.split("/")[-1]))
        pg.goto(f"{BASE}/{pagina}", wait_until="networkidle")
        pg.evaluate("[...document.images].forEach(i => i.loading = 'eager')")
        pg.wait_for_timeout(1500)

        print(f"\n-- {pagina}")
        checa(not erros_console, "sem erro de console", "; ".join(erros_console[:2]))
        checa(not falhas_rede, "sem requisição falha", "; ".join(falhas_rede[:2]))

        # imagens
        quebradas = pg.evaluate(
            "[...document.images].filter(i => i.naturalWidth === 0).map(i => i.currentSrc.split('/').pop())")
        checa(not quebradas, "todas as imagens carregam", ", ".join(quebradas[:3]))
        sem_alt = pg.evaluate("[...document.images].filter(i => !i.alt).length")
        checa(sem_alt == 0, "toda imagem tem alt", f"{sem_alt} sem alt")

        # estrutura
        hs = pg.evaluate("[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1])")
        pulos = [(hs[i - 1], hs[i]) for i in range(1, len(hs)) if hs[i] - hs[i - 1] > 1]
        checa(hs.count(1) == 1 and hs[0] == 1 and not pulos,
              "cabeçalhos em ordem, um h1 só", f"h1={hs.count(1)} pulos={pulos}")
        checa(pg.evaluate("document.documentElement.lang") == "pt-BR", "lang pt-BR")

        # metadados
        # getAttribute e não .href: o DOM resolve o link e devolve o host em
        # minúsculas, o que fazia a checagem do domínio reservado nunca casar.
        meta = pg.evaluate("""() => {
          const g = s => { const e = document.querySelector(s);
                           return e && (e.getAttribute('content') || e.getAttribute('href')) || null; };
          return { titulo: document.title, desc: g('meta[name=description]'),
                   canonical: g('link[rel=canonical]'), ogImg: g('meta[property="og:image"]'),
                   ogTitulo: g('meta[property="og:title"]') };
        }""")
        checa(bool(meta["titulo"]) and len(meta["titulo"]) <= 70, "título presente e curto",
              f"{len(meta['titulo'] or '')} caracteres")
        checa(bool(meta["desc"]) and 80 <= len(meta["desc"]) <= 170, "description no tamanho útil",
              f"{len(meta['desc'] or '')} caracteres")
        checa(bool(meta["canonical"]), "canonical presente")
        checa(bool(meta["ogImg"]) and bool(meta["ogTitulo"]), "Open Graph presente")
        reservado = [v for v in (meta["canonical"], meta["ogImg"], meta["ogTitulo"])
                     if v and "dominio-a-definir" in v.lower()]
        if reservado:
            avisa(f"{pagina}: domínio ainda é o de espaço reservado",
                  "rode tools/definir-dominio.py antes de publicar")

        # dados estruturados
        blocos = pg.evaluate(
            "[...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s => s.textContent)")
        tipos = []
        for bruto in blocos:
            try:
                tipos.append(json.loads(bruto).get("@type"))
            except json.JSONDecodeError as e:
                falhas.append(f"JSON-LD inválido em {pagina}")
                print(f"  [FALHA] JSON-LD inválido — {e}")
        checa(bool(tipos), "dados estruturados presentes", str(tipos))

        # WhatsApp
        pontos = pg.evaluate("""() => [...document.querySelectorAll('[data-whatsapp]')]
            .map(a => ({ href: a.getAttribute('href'), oculto: a.hasAttribute('hidden') }))""")
        ativos = [p for p in pontos if (p["href"] or "").startswith("https://wa.me/")]
        checa(pontos and len(ativos) == len(pontos),
              f"todos os {len(pontos)} pontos de WhatsApp ativos", f"{len(ativos)} ativos")
        if ativos:
            checa("?text=" in ativos[0]["href"], "link do WhatsApp leva mensagem pré-preenchida")
        fab = pg.evaluate("(() => { const f = document.querySelector('.aq-fab'); return f && !f.hidden; })()")
        checa(bool(fab), "botão flutuante visível")

        # links internos
        internos = {h for h in links(pg) if h.endswith(".html")}
        for h in sorted(internos):
            try:
                codigo = urllib.request.urlopen(f"{BASE}/{h}", timeout=10).getcode()
            except urllib.error.URLError as e:
                codigo = str(e)
            checa(codigo == 200, f"link interno {h}", str(codigo))

        # âncoras
        ancoras = {h for h in links(pg) if h.startswith("#") and h != "#"}
        for a in sorted(ancoras):
            existe = pg.evaluate(f"!!document.querySelector({json.dumps(a)})")
            checa(existe, f"âncora {a} existe na página")

        externos |= {h for h in links(pg) if h.startswith("http")}
        pg.close()

    # menu responsivo
    print("\n-- menu responsivo")
    pg = nav.new_page(viewport={"width": 390, "height": 844})
    pg.goto(f"{BASE}/index.html", wait_until="networkidle")
    pg.click("[data-bs-toggle=offcanvas]")
    pg.wait_for_timeout(700)
    checa(pg.locator("#aqMenu").is_visible(), "menu abre no celular")
    checa(pg.evaluate("document.querySelector('#aqMenu').contains(document.activeElement)"),
          "foco vai para dentro do menu")
    alturas = pg.evaluate(
        "[...document.querySelectorAll('.aq-nav .nav-link')].map(e => e.getBoundingClientRect().height)")
    checa(all(h >= 44 for h in alturas), "itens do menu com alvo de toque confortável",
          f"menor {min(alturas):.0f}px")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)
    checa(not pg.locator("#aqMenu").is_visible(), "menu fecha com Esc")
    checa(pg.evaluate("document.activeElement.classList.contains('aq-toggler')"),
          "foco volta para o botão do menu")
    pg.close()

    # mapa sob clique
    print("\n-- mapa")
    pg = nav.new_page(viewport={"width": 1280, "height": 900})
    terceiros = []
    pg.on("request", lambda r: terceiros.append(r.url) if "google" in r.url else None)
    pg.goto(f"{BASE}/contato.html", wait_until="networkidle")
    pg.wait_for_timeout(600)
    checa(len(terceiros) == 0, "nada de terceiros antes do clique", f"{len(terceiros)} requisições")
    altura_antes = pg.evaluate("Math.round(document.querySelector('[data-mapa]').getBoundingClientRect().height)")
    pg.get_by_role("button", name="Ver no mapa").click()
    pg.wait_for_timeout(3000)
    checa(pg.evaluate("!!document.querySelector('[data-mapa] iframe')"), "mapa carrega ao clicar")
    altura_depois = pg.evaluate("Math.round(document.querySelector('[data-mapa]').getBoundingClientRect().height)")
    checa(altura_antes == altura_depois, "mapa não desloca o layout",
          f"{altura_antes}px -> {altura_depois}px")
    pg.close()

    # rolagem horizontal
    print("\n-- resoluções")
    rolou = []
    for pagina in PAGINAS:
        for largura in LARGURAS:
            pg = nav.new_page(viewport={"width": largura, "height": 800})
            pg.goto(f"{BASE}/{pagina}", wait_until="networkidle")
            if pg.evaluate("(() => { window.scrollTo(9999, 0); return window.scrollX; })()"):
                rolou.append(f"{pagina}@{largura}")
            pg.close()
    checa(not rolou, f"sem rolagem horizontal em {len(PAGINAS) * len(LARGURAS)} combinações",
          ", ".join(rolou[:3]))

    return externos


def checa_externos(urls):
    seccao("Links externos")
    for u in sorted(urls):
        if u.startswith("https://wa.me/"):
            numero = re.search(r"wa\.me/(\d+)", u)
            checa(bool(numero) and 12 <= len(numero.group(1)) <= 13,
                  f"WhatsApp bem formado ({numero.group(1) if numero else '?'})")
            continue
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            codigo = urllib.request.urlopen(req, timeout=15).getcode()
        except Exception as e:  # noqa: BLE001 — rede é instável, o aviso basta
            avisa(f"não deu para verificar {u[:60]}", str(e)[:40])
            continue
        checa(codigo < 400, f"{u[:60]} responde", str(codigo))


def main():
    with sync_playwright() as p:
        externos = rodar(p.chromium.launch(), "Chromium")
        try:
            firefox = p.firefox.launch()
        except Exception:  # noqa: BLE001
            avisa("Firefox não instalado", "python3 -m playwright install firefox")
        else:
            rodar(firefox, "Firefox")
            firefox.close()
    checa_externos(externos)

    seccao("Resultado")
    print(f"  falhas: {len(falhas)}")
    print(f"  avisos: {len(avisos)}")
    for a in avisos:
        print(f"    - {a}")
    if falhas:
        print("\n  NÃO PUBLICAR — corrija as falhas acima.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
