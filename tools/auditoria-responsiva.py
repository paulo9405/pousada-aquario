"""
Auditoria de responsividade — critérios da seção 19 do roadmap.

Percorre as quatro páginas em oito larguras e reporta rolagem horizontal,
texto cortado, alvo de toque pequeno, imagem deformada, texto miúdo,
sobreposição do botão flutuante e linha de leitura longa demais.

Como rodar:

    python3 -m http.server 8899 --bind 127.0.0.1 &
    python3 tools/auditoria-responsiva.py          # estado atual
    python3 tools/auditoria-responsiva.py --wa     # simulando WhatsApp confirmado

Requer: pip install playwright && playwright install chromium

Saída vazia ("nenhum problema encontrado") é o resultado esperado.
"""
from playwright.sync_api import sync_playwright
import sys, json

PAGES = ["index.html", "acomodacoes.html", "pousada.html", "contato.html"]
LARGURAS = [320, 375, 390, 430, 768, 1024, 1280, 1440]
BASE = "http://127.0.0.1:8899"
COM_WHATSAPP = "--wa" in sys.argv

JS = r"""
() => {
  const out = { cortados: [], alvos: [], deformadas: [], minusculos: [], sobrepostos: [], linhas: [] };
  const vis = el => {
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0' && r.width > 0 && r.height > 0;
  };
  const nome = el => el.tagName.toLowerCase() +
    (el.id ? '#' + el.id : '') +
    (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0,2).join('.') : '');

  // 1. textos cortados: conteúdo maior que a caixa, com overflow escondido
  document.querySelectorAll('body *').forEach(el => {
    if (!vis(el)) return;
    const s = getComputedStyle(el);
    if (s.overflowX !== 'hidden' && s.overflowX !== 'clip') return;
    if (el.scrollWidth > el.clientWidth + 1 && el.textContent.trim().length > 0
        && !el.querySelector('img') && el.children.length === 0) {
      out.cortados.push({ el: nome(el), scrollW: el.scrollWidth, clientW: el.clientWidth,
                          texto: el.textContent.trim().slice(0, 40) });
    }
  });

  // 2. alvos de toque pequenos (botões, ícones e links de bloco)
  document.querySelectorAll('a, button, [role="button"]').forEach(el => {
    if (!vis(el)) return;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    const inline = s.display.startsWith('inline') && !s.display.includes('flex') &&
                   el.closest('p, li, figcaption, dd, dt');
    if (inline) return;                       // link dentro de texto corrido não é alvo de botão
    if (r.height < 44 || r.width < 24) {
      out.alvos.push({ el: nome(el), w: Math.round(r.width), h: Math.round(r.height),
                       texto: el.textContent.trim().slice(0, 30) });
    }
  });

  // 3. imagens deformadas: proporção renderizada != natural, sem object-fit
  [...document.images].forEach(img => {
    if (!vis(img) || !img.naturalWidth) return;
    const s = getComputedStyle(img);
    if (s.objectFit === 'cover' || s.objectFit === 'contain') return;
    const r = img.getBoundingClientRect();
    const pNat = img.naturalWidth / img.naturalHeight, pRen = r.width / r.height;
    if (Math.abs(pNat - pRen) / pNat > 0.02) {
      out.deformadas.push({ src: img.src.split('/').pop(),
                            natural: pNat.toFixed(3), renderizada: pRen.toFixed(3) });
    }
  });

  // 4. texto pequeno demais
  document.querySelectorAll('body *').forEach(el => {
    if (!vis(el) || el.children.length) return;
    const t = el.textContent.trim();
    if (!t) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 12) out.minusculos.push({ el: nome(el), fs, texto: t.slice(0, 30) });
  });

  // 5. sobreposição do botão flutuante sobre conteúdo clicável ou texto
  const fab = document.querySelector('.aq-fab');
  if (fab && !fab.hidden && vis(fab)) {
    const f = fab.getBoundingClientRect();
    document.querySelectorAll('a:not(.aq-fab), button, p, h1, h2, h3, dd, dt').forEach(el => {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      if (r.right > f.left && r.left < f.right && r.bottom > f.top && r.top < f.bottom) {
        out.sobrepostos.push({ el: nome(el), texto: el.textContent.trim().slice(0, 30) });
      }
    });
  }

  // 6. linha de leitura longa demais
  const ctx = document.createElement('canvas').getContext('2d');
  document.querySelectorAll('p').forEach(el => {
    if (!vis(el) || el.textContent.trim().length < 80) return;
    const s = getComputedStyle(el);
    // mede o glifo "0" na fonte real do elemento em vez de estimar 0.5em
    ctx.font = `${s.fontStyle} ${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
    const ch = el.getBoundingClientRect().width / ctx.measureText('0').width;
    if (ch > 85) out.linhas.push({ el: nome(el), ch: Math.round(ch),
                                   texto: el.textContent.trim().slice(0, 35) });
  });

  return out;
}
"""

def rodar():
    achados = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for page in PAGES:
            for w in LARGURAS:
                pg = b.new_page(viewport={"width": w, "height": 800})
                if COM_WHATSAPP:
                    pg.route("**/js/main.js", lambda r: r.fulfill(
                        status=200, content_type="application/javascript; charset=utf-8",
                        body=open("js/main.js", encoding="utf-8")
                             .read().replace("whatsapp: ''", "whatsapp: '5538999999999'")))
                pg.goto(f"{BASE}/{page}", wait_until="networkidle")
                pg.evaluate("[...document.images].forEach(i => i.loading = 'eager')")
                pg.wait_for_timeout(900)
                # rola até o fim de verdade: as imagens lazy crescem a página
                # depois do primeiro scroll, e medir antes disso deixa
                # conteúdo do meio embaixo do botão flutuante
                for _ in range(4):
                    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    pg.wait_for_timeout(400)
                r = pg.evaluate(JS)
                r["rolagem_h"] = pg.evaluate("(()=>{window.scrollTo(9999,0);return window.scrollX})()")
                for k, v in r.items():
                    if v:
                        achados.setdefault(k, []).append((page, w, v))
                pg.close()
        b.close()
    return achados

achados = rodar()
rotulos = {
    "rolagem_h": "ROLAGEM HORIZONTAL",
    "cortados": "TEXTO CORTADO",
    "alvos": "ALVO DE TOQUE < 44px",
    "deformadas": "IMAGEM DEFORMADA",
    "minusculos": "TEXTO < 12px",
    "sobrepostos": "BOTÃO FLUTUANTE SOBRE CONTEÚDO",
    "linhas": "LINHA > 85 caracteres",
}
if not achados:
    print("nenhum problema encontrado")
for k, lista in achados.items():
    print(f"\n### {rotulos.get(k, k)} — {len(lista)} ocorrência(s)")
    vistos = set()
    for page, w, v in lista:
        chave = json.dumps(v, sort_keys=True)[:200]
        if chave in vistos: continue
        vistos.add(chave)
        print(f"  {page} @{w}px: {json.dumps(v, ensure_ascii=False)[:300]}")
