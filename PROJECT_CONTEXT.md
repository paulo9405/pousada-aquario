# Contexto do projeto — Hotel Pousada Aquários

Memória técnica e de produto. Leia antes de alterar qualquer coisa relevante.

Última revisão: 01/09/2026 · commit de referência: `d1b6711`

---

## 1. Contexto

### O que é

Site institucional estático da **Hotel Pousada Aquários**, pousada em
Buritizeiro/MG, às margens do Rio São Francisco.

### Para quem

Cliente final: **Roney**, proprietário da pousada.

### Situação comercial — importante

**Este site nasceu como protótipo funcional para apresentar uma proposta de
trabalho ao proprietário.** Ele ainda não foi contratado nem validado por ele.

Isso muda como o conteúdo deve ser tratado: boa parte das informações no ar
hoje é provisória, veio de fontes públicas ou do material de divulgação da
própria pousada, e **nada disso foi confirmado**. Ver a seção 6.

### Problema comercial que resolve

A pousada tem presença no Google com avaliações, mas presença digital
limitada. O site é canal próprio para:

```text
Google / Instagram / indicação → Site → WhatsApp → reserva
```

**Não é sistema de reservas.** O objetivo é converter visitante em conversa no
WhatsApp, onde disponibilidade e valores são tratados pela pousada.

### Público

Turistas, casais, famílias, gente visitando parentes, viajantes de passagem,
profissionais em trabalho temporário na região e empresas hospedando
funcionários.

---

## 2. Estratégia geográfica — Buritizeiro e Pirapora

**Esta é a decisão de produto mais importante do projeto.**

A pousada fica em **Buritizeiro/MG**. **Pirapora/MG** é a cidade vizinha, do
outro lado do Rio São Francisco, ligada pela **Ponte Marechal Hermes**. Quem
procura hospedagem em Pirapora tem na pousada uma alternativa a poucos minutos.

O site trabalha as duas cidades organicamente:

- `areaServed` no Schema.org lista Buritizeiro **e** Pirapora
- `address` no Schema.org tem **apenas Buritizeiro** — declarar endereço em
  Pirapora seria falsear localização, e o Google penaliza como spam local
- Títulos e meta descriptions das quatro páginas citam as duas cidades
- O H2 da home lidera com a proximidade: *"A apenas 13 minutos a pé do centro
  de Pirapora"*
- A primeira pergunta frequente da página de contato é literalmente
  *"A pousada fica em Pirapora?"*, respondida com a verdade

**Regra permanente:** nunca alterar o endereço para tentar ranquear em
Pirapora. A proximidade se comunica por conteúdo, não por dado falso.

**Expectativa realista:** para busca de hospedagem, quem domina o topo é o
bloco de mapa, alimentado pelo **Google Business Profile**, não pelo site.
Disputar "hotel em Pirapora" de igual para igual com hotéis dentro de Pirapora
não é realista. O site ajuda em "perto de Pirapora" e "Pirapora e região".

---

## 3. Stack e arquitetura

### Tecnologias

```text
HTML5 · CSS3 · Bootstrap 5.3.8 · JavaScript vanilla · Cloudflare Pages
```

**Sem etapa de build.** Os arquivos são servidos como estão. Sem backend, sem
banco, sem framework de front, sem SPA.

Tudo é servido do próprio domínio — Bootstrap em `vendor/`, fonte em `fonts/`.
Nenhuma requisição a terceiros no carregamento: pelo CDN o navegador abria uma
segunda conexão (DNS + TLS) no caminho crítico.

Os ícones são **SVG inline**. A fonte do Bootstrap Icons custava 87 KB de CSS
mais 134 KB de fonte para 21 símbolos.

Usa `bootstrap.min.js`, **não** o bundle: o bundle embute o Popper, que só
serve a dropdown, tooltip e popover. O site usa apenas o offcanvas.

### Estrutura

```text
pousada-aquarios/
├── index.html            Início
├── acomodacoes.html      Acomodações
├── pousada.html          A Pousada
├── contato.html          Localização e contato
├── 404.html              Erro (noindex)
├── styleguide.html       Design system, referência interna (noindex)
├── css/style.css         Design system completo, 27 seções
├── js/main.js            Configuração e comportamentos
├── fonts/                Figtree variável (woff2, self-hosted)
├── vendor/               Bootstrap CSS e JS
├── img/                  Fotos, logo e variantes responsivas
├── tools/                Scripts de desenvolvimento (fora do deploy)
├── docs/                 Documentação interna (NÃO versionada, ver .gitignore)
├── _headers              Cache do Cloudflare Pages
├── robots.txt
└── sitemap.xml
```

### Comandos

```bash
python3 tools/servidor-local.py     # http://127.0.0.1:8900
python3 tools/qa.py                 # QA completo, Chromium + Firefox
python3 tools/qa.py --wa            # simula WhatsApp configurado
python3 tools/definir-dominio.py https://novo.dominio.com.br
npx lighthouse http://127.0.0.1:8900/index.html --view
```

**Não abra os arquivos com duplo clique.** Os links são absolutos a partir da
raiz (`/contato`), que é o que o Cloudflare Pages serve sem redirecionar. No
`file://`, a raiz é a raiz do disco e tudo quebra.

O `tools/servidor-local.py` não é servidor genérico: imita o Cloudflare Pages
de propósito — compressão de texto, URL sem extensão, 308 de `/contato.html`
para `/contato` e 404 real. É o que garante que o que passa localmente passa em
produção.

### Deploy

| Item | Valor |
| ---- | ----- |
| Repositório | `paulo9405/pousada-aquario`, branch `main` |
| Plataforma | Cloudflare Pages, projeto `pousada-aquario` |
| Build | preset None, comando vazio, output `/` |
| URL do Pages | `pousada-aquario.pages.dev` |
| Domínio em uso | `https://hotelpousadaquarios.paulodev.net` |

Push na `main` dispara deploy automático.

**O domínio é provisório**: subdomínio do domínio pessoal do desenvolvedor,
para demonstração. Para SEO local, domínio próprio (`pousadaaquarios.com.br`)
vale bem mais. Ao trocar, rode `tools/definir-dominio.py` — ele atualiza as 29
URLs absolutas em HTML, sitemap e robots de uma vez.

---

## 4. Identidade visual

### Cores — `css/style.css`, seção 2

Extraídas da logo. Todos os contrastes verificados em WCAG 2.1.

| Token | HEX | Uso |
| ----- | --- | --- |
| `--aquarios-primary` | `#1A5FC2` | azul principal, links, botões — 6.07:1 com branco |
| `--aquarios-primary-hover` | `#164FA3` | hover de superfícies azuis |
| `--aquarios-primary-dark` | `#0A2F63` | títulos, rodapé — 13.1:1 |
| `--aquarios-primary-deep` | `#071E3F` | fundos escuros, cabeçalho de página — 16.6:1 |
| `--aquarios-primary-soft` | `#E8F0FB` | tinte de seção |
| `--aquarios-gold` | `#F0C419` | preenchimento e destaque, nunca texto sobre branco |
| `--aquarios-gold-hover` | `#DBB110` | hover do dourado |
| `--aquarios-gold-dark` | `#8F6006` | texto e ícones dourados — 5.46:1 com branco |
| `--aquarios-bg` | `#FFFFFF` | fundo |
| `--aquarios-bg-alt` | `#F2F6FB` | seção alternada |
| `--aquarios-text` | `#17212E` | texto — 16.2:1 |
| `--aquarios-text-muted` | `#5A6675` | texto secundário — 5.85:1 |
| `--aquarios-border` | `#DBE3EC` | bordas |
| `--aquarios-border-strong` | `#B9C6D6` | bordas com ênfase |
| `--aquarios-whatsapp` | `#0F7A6C` | superfícies de conversão — 5.22:1 |
| `--aquarios-whatsapp-hover` | `#0B6157` | hover |
| `--aquarios-whatsapp-light` | `#25D366` | verde de marca, **só sobre fundo escuro** |

**Duas armadilhas já pagas, não repetir:**

1. O verde oficial do WhatsApp `#25D366` tem **1.98:1** com branco. Reprova em
   WCAG para texto e para componentes. Por isso as superfícies clicáveis usam
   `#0F7A6C`.
2. `--aquarios-gold-dark` era `#C9880A` (3.00:1), documentado como "só texto
   grande". Foi usado em `.aq-eyebrow`, que é **13px bold** — e bold de 13px
   **não** conta como texto grande em WCAG (o limite é 18,66px). O Lighthouse
   pegou. Hoje é `#8F6006`.

O dourado nunca deve dominar a interface.

### Tipografia

**Figtree variável**, self-hosted em `fonts/`. Um arquivo de ~20 KB no subset
latin cobre os pesos 300–900. `font-display: swap`, com `preload` do subset
latin em todas as páginas.

Escala fluida com `clamp()`, sem breakpoints:

```css
--aquarios-fs-h1:   clamp(2rem,      1.35rem + 3.2vw, 3.5rem);
--aquarios-fs-h2:   clamp(1.625rem,  1.28rem + 1.7vw, 2.5rem);
--aquarios-fs-h3:   clamp(1.25rem,   1.10rem + 0.7vw, 1.625rem);
--aquarios-fs-h4:   clamp(1.125rem,  1.06rem + 0.3vw, 1.3125rem);
--aquarios-fs-lead: clamp(1.0625rem, 1rem + 0.35vw,   1.25rem);
--aquarios-fs-body: 1rem;  --aquarios-fs-sm: 0.9375rem;  --aquarios-fs-xs: 0.8125rem;
```

Alturas de linha: `1.15` títulos, `1.35` intermediária, `1.65` corpo.

**Detalhe que já causou erro de medição:** o glifo "0" da Figtree tem
**0,640em**, não 0,5em. Cálculo de comprimento de linha precisa medir a fonte
real com `measureText`, não estimar.

### Espaçamento, bordas, layout

```css
--aquarios-space-3xs .25rem   --aquarios-space-2xs .5rem    --aquarios-space-xs .75rem
--aquarios-space-sm  1rem     --aquarios-space-md  1.5rem   --aquarios-space-lg 2.5rem
--aquarios-space-xl  4rem     --aquarios-space-2xl 6rem

--aquarios-section-y     clamp(3rem, 2rem + 5vw, 6rem)
--aquarios-section-y-sm  clamp(2rem, 1.5rem + 3vw, 3.5rem)

--aquarios-radius-sm .375rem  --aquarios-radius .75rem  --aquarios-radius-lg 1.25rem
--aquarios-container 1200px   --aquarios-measure 68ch    --aquarios-tap 2.75rem
--aquarios-transition 180ms cubic-bezier(.2, .6, .3, 1)
```

Sombras com base azulada (`rgba(7,30,63,…)`), para não cinzar a interface.

### Logo e assets

- `img/logo.png` — original, 1536×1024, **fonte**, não é servida
- `img/logo-nav-180.webp`, `-360.webp`, `logo-nav@2x.webp` — header, recortadas
  na caixa alfa e otimizadas. 12 KB no tamanho servido, contra 1,5 MB do PNG
- `favicon.ico` e `apple-touch-icon.png` — derivados do motivo da logo. **A
  logo inteira vira borrão a 16px** porque tem texto; o ícone usa a gaivota em
  tile azul. É interpretação, não a marca oficial — validar com o proprietário
- No rodapé a marca aparece **como texto**: o lettering preto da logo sumiria
  no azul profundo

---

## 5. Padrões de UI e responsividade

### Componentes — `css/style.css`

Botões: `.btn-aq` (primário) · `.btn-aq-outline` · `.btn-aq-outline--invert`
(sobre foto/fundo escuro) · `.btn-aq-gold` (destaque sobre escuro) ·
`.btn-aq-whatsapp` · tamanhos `.btn-aq-lg` / `.btn-aq-sm` / `.btn-aq-block`.
Todos com **44px de altura mínima**.

Estrutura: `.aq-header` (sticky) · `.aq-nav` · `.aq-offcanvas` · `.aq-pagehead`
· `.aq-section` · `.aq-section-head` · `.aq-footer` · `.aq-fab`

Conteúdo: `.aq-card` · `.aq-media` (proporções fixas) · `.aq-mosaic` ·
`.aq-gallery` · `.aq-specs` (ficha de dados) · `.aq-empty` (estado vazio) ·
`.aq-pill` · `.aq-list` · `.aq-rule` · `.aq-rating` · `.aq-map` · `.aq-icon`

`styleguide.html` mostra o sistema inteiro renderizado. Está `noindex`, fora do
menu e bloqueado no `robots.txt`.

### Breakpoints

```text
575.98px   telas estreitas: botões do hero em largura cheia, véu do hero mais forte
767.98px   mosaico e galeria mudam de colunas
991.98px   menu vira offcanvas; abaixo disso, alvos de toque maiores
520px alt  tela baixa (celular deitado, zoom 200%): hero encolhe respiro e título
```

Mais `(hover: hover)` para elevação de card e `(prefers-reduced-motion)`.

### Regras de responsividade que não podem regredir

- **Zero rolagem horizontal** em qualquer largura. Testar com `window.scrollX`
  depois de tentar rolar, **não** com `scrollWidth` — com o offcanvas fechado,
  `scrollWidth` dá falso positivo
- **CTA do hero visível na primeira tela** em toda largura, incluindo celular
  deitado e zoom de 200%
- Alvos de toque com no mínimo 44px
- Linha de leitura até ~85 caracteres

### Header

Sticky em todas as telas. Ganha sombra e borda depois que a página rola
(`.aq-header--scrolled`, aplicada por `initHeader()` com `requestAnimationFrame`
e listener passivo). Navegação em offcanvas abaixo de 992px, barra horizontal
acima.

**Não colocar `backdrop-filter` no header.** Ele cria bloco de contenção para
descendentes `position: fixed`, e o offcanvas do menu passa a medir a altura do
header em vez da viewport — o menu abre com 90px de altura. Já aconteceu.

### Hero e contraste sobre foto

O texto do hero é branco sobre foto, com véu em gradiente. **O contraste é
medido nos pixels compostos**, não estimado: esconde-se o texto, fotografa-se o
fundo e calcula-se o contraste do branco contra cada pixel atrás de cada bloco.

Estado atual: **pior caso 5,97:1** em 10 viewports.

Aprendizados que valem para qualquer troca de foto:

- O véu escurece **mais à esquerda** (onde o texto fica) e **menos embaixo**.
  A versão anterior gastava opacidade no pé da imagem, onde não há texto —
  escurecer por altura dava menos contraste E menos foto visível
- Telas estreitas têm regra própria (véu quase uniforme): as paradas do
  gradiente são relativas à altura, e num hero baixo o texto sobe para a faixa
  clara
- O eyebrow do hero é **branco, não dourado**: medido sobre a foto, o dourado
  dava 3,5:1 no mobile. E o hero troca de foto, então o texto não pode depender
  do brilho da imagem
- **Ao trocar a foto do hero, refazer a medição.** Não confie no olho

---

## 6. Conteúdo — o que é real e o que é provisório

**Regra central do projeto: nada não confirmado é apresentado como fato.**

Todo conteúdo pendente está marcado no HTML com `data-confirmar`. Para listar:

```bash
grep -rn "data-confirmar" *.html
```

Para revisar visualmente, adicione a classe `aq-revisao` ao `<body>`: todos os
pontos pendentes ficam destacados na tela.

### Confirmado com o proprietário

| Item | Valor |
| ---- | ----- |
| Endereço | Av. Barnabé Martins, 133 — Buritizeiro/MG, 39280-000 |
| Referência | Próximo à Ponte Marechal Hermes |
| WhatsApp / telefone | (31) 99520-6536 |
| Check-in / check-out | 12h / 12h |
| Café da manhã | Das 7h às 10h |
| Aceita animais | Sim |
| Formas de pagamento | Dinheiro, cartão e Pix |
| Distância até Pirapora | ~13 min a pé, ~4 min de bicicleta até o centro (fonte: Google Maps) |

A pousada fica separada do rio por uma rua — "às margens" é uso correto em
hospedagem. O limite fica um degrau acima: **não** afirmar "pé na água",
"acesso direto ao rio" ou "o rio nos fundos".

A vista do rio é afirmada **a partir da varanda**, o que a legenda gravada pela
própria pousada em `img/area-vista-rio.webp` sustenta. **Vista a partir dos
quartos nunca foi confirmada e não é afirmada em lugar nenhum.**

### Provisório — precisa do proprietário

| Item | Situação atual no site |
| ---- | ---------------------- |
| Categorias de quarto | Estado vazio. Nome, capacidade, cama, comodidades e preço não existem. O modelo de card pronto para preencher está em comentário no HTML de `acomodacoes.html` |
| Política de crianças | "a confirmar" |
| Cancelamento | "a confirmar" |
| Acessibilidade | "a confirmar" |
| E-mail | "a confirmar" no rodapé e no card de contato |
| História da pousada | Estado vazio em `pousada.html` |
| Nota do Google (4,4) | Exibida, marcada como não confirmada. **Nenhuma avaliação é reproduzida** |
| Lista de comodidades | Ar-condicionado, TV, frigobar, garagem, ducha quente/fria, colchões ortopédicos, enxoval novo — vieram do **folheto de divulgação da própria pousada** (`img/area-externa.webp`), não confirmados um a um |
| Telefones extras | O folheto traz (38) 99156-7590 e (38) 98843-9676. Não estão no site |

Detalhe: `img/area-externa.webp` **não é foto da pousada** — é o folheto de
divulgação, com telefones e e-mail. Nenhuma página o usa. Como o repositório é
público e ele carrega dados de contato, considerar movê-lo para `docs/`.

### Fotos — todas provisórias

As imagens atuais foram feitas pela própria pousada e **serão substituídas por
sessão fotográfica profissional**. A arquitetura já suporta a troca: a
proporção fica no container (`.aq-media`), não no arquivo.

Pendências conhecidas de imagem:

- `img/area-vista-rio.webp` tem legenda amarela gravada por cima
- **Não existe nenhuma foto da fachada** da pousada
- Cada categoria de quarto precisa ser fotografada separadamente

**Foto de capa.** O hero usa `img/paisagem-ponte-marechal.png` (2048×768),
da Ponte Marechal Hermes ao pôr do sol. **Fotografia autoral do desenvolvedor
do site** — sem questão de licença.

No mesmo diretório existem duas versões auxiliares do mesmo enquadramento,
`img/ponte-marechal-mg-635x421.jpg` e
`img/ChatGPT Image 1 de set. de 2026, 09_33_37.png`. Nenhuma página as usa;
ficam como material de apoio. Só a `paisagem-ponte-marechal.png` gera as
variantes servidas (`hero-ponte-wide-*` e `hero-ponte-tall-*`).

---

## 7. Funcionalidades

### WhatsApp — principal caminho de conversão

Número em `js/main.js`, em **um único lugar**:

```js
const AQUARIOS = {
  whatsapp: '5531995206536',
  whatsappMessage: 'Olá! Vim pelo site e gostaria de fazer uma reserva.',
};
```

`initWhatsApp()` monta o link `wa.me`, aplica em todos os elementos marcados
com `data-whatsapp` (ajusta `href`, `target`, `rel`), revela o botão flutuante
e acrescenta a classe `aq-com-fab` ao `<body>` — que reserva no rodapé a faixa
ocupada pelo botão, para ele não cobrir texto no fim da página.

**Esvaziar `whatsapp` tira o WhatsApp do ar por completo:** os botões voltam ao
`href` de fallback e o flutuante some. A exceção é o botão do card de contato,
que tem o link escrito direto no HTML para funcionar sem JavaScript.

Mensagem curta de propósito. A versão original do roadmap pedia um formulário
de check-in/check-out/hóspedes dentro da mensagem — obriga o hóspede a
preencher três campos no WhatsApp e atrapalha mais que ajuda.

### Mapa — carrega sob clique

`initMapa()` só insere o iframe do Google depois do clique. O iframe puxa **18
requisições de terceiros**, e quem só quer o endereço ou o botão de rota não
deveria pagar por isso. O espaço reservado tem a mesma altura do mapa, então
não há salto de layout na troca.

### Outros

`initHeader()` — sombra do header ao rolar. `initAnoAtual()` — ano no rodapé.

Menu offcanvas do Bootstrap: fecha com Esc, prende o foco e devolve o foco ao
botão ao fechar.

---

## 8. SEO

### Implementado

- Título único e meta description em todas as páginas (~60 e ~155 caracteres)
- Canonical **absoluto** em todas — relativo o Google aceita, mas o Lighthouse
  reprova com `Is not an absolute URL` e derruba o SEO de 100 para 92
- Open Graph completo e Twitter Card
- `img/og-image.jpg` (1200×630) — prévia de compartilhamento. **Ainda é a foto
  antiga do amanhecer, não a capa nova**
- `robots.txt` bloqueando `/styleguide` e `/tools/`
- `sitemap.xml` com as quatro páginas
- HTML semântico, `lang="pt-BR"`, `h1` único por página, sem pulo de nível
- `alt` em todas as imagens

### Dados estruturados

| Página | Blocos JSON-LD |
| ------ | -------------- |
| `index.html` | `LodgingBusiness` |
| `contato.html` | `LodgingBusiness`, `BreadcrumbList`, `FAQPage` |
| `acomodacoes.html` | `BreadcrumbList` |
| `pousada.html` | `BreadcrumbList` |

O `LodgingBusiness` declara: nome, descrição, url, image, logo, `telephone`,
`address` completo, `hasMap`, `areaServed` (Buritizeiro + Pirapora),
`checkinTime`, `checkoutTime`, `petsAllowed`, `currenciesAccepted`,
`paymentAccepted` e `amenityFeature`.

**Fora de propósito**, por dependerem de dado não confirmado: `geo` (sem
coordenadas verificadas), `priceRange` e `aggregateRating`.

O `FAQPage` tem as três respostas visíveis na página, como o Google exige.

### URLs

O Cloudflare Pages serve **URL sem extensão** e redireciona `.html` com 308:

```text
/contato.html → 308 → /contato
/index.html   → 308 → /
```

Links internos, canonical, Open Graph e sitemap usam a forma **sem extensão**.
Redirecionamento em link interno custa uma viagem a cada clique; em canonical,
faz o Google ver URL diferente da declarada. **Isso foi um bug real no primeiro
deploy** — passou no QA porque o servidor local entregava `.html` direto.

### NAP — precisa bater com o Google Business Profile

```text
Hotel Pousada Aquários
Av. Barnabé Martins, 133 — Buritizeiro/MG, 39280-000
(31) 99520-6536
```

---

## 9. Performance

Lighthouse mobile, servido com compressão: **100 em Performance,
Acessibilidade, Boas Práticas e SEO nas quatro páginas.** Home com LCP 1,9s,
TBT 0, CLS 0, ~289 KiB.

**Medir sempre com `tools/servidor-local.py`.** O `python3 -m http.server` não
comprime e derruba a nota artificialmente — a primeira medição deu 84 e levou a
otimizar o que já estava resolvido.

O que trouxe o ganho:

- Ícones em SVG inline no lugar da fonte de ícones (−221 KB)
- `bootstrap.min.js` no lugar do bundle (−20 KB)
- **Imagens recortadas na proporção de exibição.** O mosaico é 1:1 e a galeria
  4:3; antes o navegador baixava a foto vertical inteira para o `object-fit`
  descartar metade dos pixels
- `srcset` e `sizes` em todas as fotos, com degraus de 180 a 2048px
- Bootstrap e fonte no próprio domínio

`_headers` define o cache: um ano com `immutable` para `img/`, `fonts/` e
`vendor/`; um dia para `css/` e `js/`; revalidação a cada visita para HTML.

**AVIF ficou de fora** — o ambiente de desenvolvimento não tinha codificador.
Vale gerar junto com as fotos definitivas.

`img/` tem 11 MB no repositório, mas só ~2,3 MB são servidos. O resto são
originais mantidos como fonte para regerar variantes.

---

## 10. Qualidade — como verificar antes de publicar

```bash
python3 tools/servidor-local.py &
python3 tools/qa.py
```

**195 verificações, em Chromium e Firefox.** Qualquer `[FALHA]` impede a
publicação. Cobre: estrutura de tags do HTML, links internos e âncoras, links
externos, WhatsApp, mapa, menu, imagens, `alt`, metadados, dados estruturados,
ordem de cabeçalhos, 404 e rolagem horizontal em oito larguras.

Três checagens nasceram de bugs reais que passaram por todo o resto:

1. **Link interno e canonical respondendo 200 sem redirecionar** — o site subiu
   com 308 em toda navegação
2. **Caminho inexistente devolvendo 404** — sem `404.html`, o Pages devolvia
   **200 com a home**, e o Google indexaria endereços inventados
3. **Tags equilibradas** — uma `</div>` fechada cedo demais deixou quatro cards
   fora da grade, renderizando em largura cheia. O site tinha Lighthouse 100,
   zero erro de console e nenhuma rolagem horizontal

`tools/auditoria-responsiva.py` roda a auditoria de responsividade isolada.

---

## 11. Regras para futuras alterações

1. **Não executar `git commit` nem `git push`.** Os commits são feitos
   manualmente pelo proprietário do projeto. Ao concluir, informar os arquivos
   para o stage, a mensagem em Conventional Commits e os comandos.
2. **Não inventar dado da pousada.** Se não foi confirmado, marcar com
   `data-confirmar` e mostrar como pendente.
3. **Não alterar endereço, telefone ou preços** sem confirmação.
4. **Não declarar endereço em Pirapora** no Schema.org.
5. **Ao trocar foto do hero, refazer a medição de contraste** nos pixels
   compostos, em pelo menos 8 viewports, incluindo 320px e celular deitado.
6. **Rodar `tools/qa.py` antes de qualquer publicação.**
7. **Testar com `tools/servidor-local.py`**, nunca abrindo o arquivo direto.
8. Evitar dependência nova. A regra do projeto é simplicidade: recurso extra só
   entra com benefício real ao usuário.
9. Não prometer luxo, "melhor da região" nem nada não verificável. "Bom
   custo-benefício" pode; "barata" não.
10. Evitar termos que sinalizam deficiência no texto voltado ao hóspede —
    "simples", "de bairro", "modesta". Em português de hospedagem funcionam
    como eufemismo de avaliação negativa. Usar termos que descrevem o benefício
    real: tranquila, acolhedora, familiar.

---

## 12. Estado atual e próximos passos

### Concluído

As dez fases do roadmap (`docs/Roadmap_Implementacao.md`): setup, design
system, header e navegação, home, acomodações, institucional e localização,
responsividade, performance, SEO local e QA. Site publicado, domínio ativo,
HTTPS e deploy automático funcionando.

### O que depende da conversa com o proprietário

**O site está no estágio de protótipo por opção, não por falta de trabalho
técnico.** A conversa com o Roney ainda não aconteceu, e é ela que vai
destravar o conteúdo comercial. Os espaços já estão construídos e esperando o
dado — estado vazio nas categorias, ficha de regras com os campos, espaço
reservado para a história.

**Um agente que abrir este projeto não deve preencher esses espaços por conta
própria.** Estado vazio bem feito é melhor que dado inventado: o protótipo
serve justamente para mostrar ao proprietário onde cada informação entra.

O checklist completo está em `docs/Informacoes-a-confirmar-com-Roney.md`. O
item de maior peso comercial são as **categorias de quarto** — nome,
capacidade, cama, comodidades e preço.

### Pendências técnicas menores

- `img/og-image.jpg` ainda usa a foto antiga do amanhecer
- Mover `img/area-externa.webp` (folheto com telefones) para `docs/`
- Gerar variantes AVIF quando houver codificador

### Depois da conversa com o proprietário

- Sessão fotográfica e substituição de todas as imagens
- Domínio próprio, com `tools/definir-dominio.py`
- Google Business Profile completo, com NAP idêntico ao site — **é ele que
  alimenta o bloco de mapa, que é o que mais converte em busca local**
- Search Console: enviar sitemap e acompanhar indexação
