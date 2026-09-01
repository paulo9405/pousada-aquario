# Hotel Pousada Aquários

Site institucional da Hotel Pousada Aquários — Buritizeiro/MG, às margens do
Rio São Francisco.

Site estático, sem backend. O objetivo é converter visitantes vindos do Google,
Instagram e indicações em contato direto pelo WhatsApp.

## Stack

HTML5 · CSS3 · Bootstrap 5.3.8 · Bootstrap Icons 1.13.1 · JavaScript vanilla ·
Cloudflare Pages

Tudo é servido do próprio domínio — Bootstrap em `vendor/`, a fonte Figtree
em `fonts/`. Nenhuma requisição a terceiros: pelo CDN o navegador abria uma
segunda conexão (DNS + TLS) no caminho crítico.

Não há etapa de build: os arquivos são servidos como estão.

## Estrutura

```text
pousada-aquarios/
├── css/style.css        # design system completo
├── js/main.js           # configuração do site (contato, helpers)
├── fonts/               # Figtree variável (woff2, self-hosted)
├── vendor/              # Bootstrap CSS e JS (self-hosted)
├── tools/               # scripts de desenvolvimento (fora do deploy)
├── _headers             # cache do Cloudflare Pages
├── img/                 # fotografias e logo (provisórias)
│   ├── logo-nav.webp    # logo recortada e otimizada para o header
│   └── hero-rio-*.webp  # recortes do hero (wide para desktop, tall para mobile)
├── index.html           # Início
├── acomodacoes.html     # Acomodações
├── pousada.html         # A Pousada
├── contato.html         # Localização e contato
├── styleguide.html      # referência interna do design system (noindex)
├── robots.txt
├── sitemap.xml
├── DEPLOY.md            # passo a passo da publicação
├── favicon.ico
└── apple-touch-icon.png
```

A pasta `docs/` contém a documentação interna do projeto (roadmap e
apresentação) e não é versionada.

## Rodando localmente

Por causa dos caminhos relativos e do CDN, sirva a pasta em vez de abrir o
arquivo direto:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Design system

Tudo vive em `css/style.css`, organizado em 14 seções (fontes, tokens,
overrides do Bootstrap, base, tipografia, layout, links, botões, cards,
mídia, detalhes, acessibilidade, utilitários).

`styleguide.html` mostra o sistema inteiro renderizado — é a referência de
trabalho. Está com `noindex` e não entra no menu nem no sitemap.

### Cores

Extraídas da logo. Os contrastes foram verificados em WCAG 2.1 — as
anotações estão ao lado de cada token.

| Token                     | Valor     | Uso                              |
| ------------------------- | --------- | -------------------------------- |
| `--aquarios-primary`      | `#1A5FC2` | azul principal, links, botões    |
| `--aquarios-primary-dark` | `#0A2F63` | títulos, rodapé, overlays        |
| `--aquarios-primary-soft` | `#E8F0FB` | fundos de seção                  |
| `--aquarios-gold`         | `#F0C419` | destaque pontual (nunca dominante) |
| `--aquarios-gold-dark`    | `#8F6006` | texto e ícones dourados (AA)     |
| `--aquarios-text`         | `#17212E` | texto                            |
| `--aquarios-whatsapp`     | `#0F7A6C` | superfícies de conversão         |

O verde oficial do WhatsApp (`#25D366`) tem 1.98:1 com branco e reprova em
WCAG. Superfícies clicáveis usam `#0F7A6C`, da própria paleta do WhatsApp; o
verde claro fica reservado a ícone sobre fundo escuro.

### Tipografia

Figtree variável, self-hosted — um arquivo de ~20 KB cobre os pesos 300–900.
A escala é fluida com `clamp()`: cresce sozinha entre 320 px e 1400 px, sem
breakpoints.

### Componentes

`.btn-aq` · `.btn-aq-outline` · `.btn-aq-gold` · `.btn-aq-whatsapp` ·
`.aq-card` · `.aq-media` (proporções fixas) · `.aq-pill` · `.aq-section-head` ·
`.aq-list` · `.aq-rule` · `.aq-header` · `.aq-nav` · `.aq-fab`

Todos os botões têm no mínimo 44 px de altura. A proporção das imagens fica
no container, não no arquivo — trocar as fotos provisórias pelas definitivas
não mexe no layout.

## Contato e WhatsApp

Número confirmado: **(31) 99520-6536**, em `AQUARIOS.whatsapp` (`js/main.js`).
`initWhatsApp()` monta o link `wa.me` com a mensagem pré-preenchida — *"Olá!
Vim pelo site e gostaria de fazer uma reserva."* — e aplica em todos os pontos
marcados com `data-whatsapp`, além de revelar o botão flutuante. O número
aparece uma única vez no código.

Para tirar o WhatsApp do ar, basta esvaziar `whatsapp`: os botões voltam ao
`href` de fallback e o flutuante some. A exceção é o botão do cartão de
contato, que tem o link `wa.me` escrito direto no HTML para funcionar mesmo
com JavaScript desativado.

### Dados da pousada

| Item | Valor |
| ---- | ----- |
| Endereço | Av. Barnabé Martins, 133 — Buritizeiro/MG · 39280-000 |
| Referência | Próximo à Ponte Marechal Hermes |
| WhatsApp / telefone | (31) 99520-6536 |
| Check-in / check-out | 12h / 12h |
| Café da manhã | Das 7h às 10h |
| Aceita animais | Sim |
| Pagamento | Dinheiro, cartão e Pix |

Ainda em confirmação (`data-confirmar`): e-mail, política de crianças,
cancelamento, acessibilidade, categorias de quarto, história da pousada, a
nota do Google e a lista de comodidades vinda do material de divulgação.

## Conteúdo a confirmar

Todo dado que ainda depende de confirmação com o proprietário está marcado
com o atributo `data-confirmar`. Para revisar visualmente, adicione a classe
`aq-revisao` ao `<body>` — todos ficam destacados na tela.

Para listar tudo:

```bash
grep -rn "data-confirmar" *.html
```

Hoje isso cobre a lista de comodidades (extraída do material de divulgação da
própria pousada), a nota do Google, os canais de contato, as categorias de
quarto, as regras da hospedagem, a história da pousada e o endereço.

## Status

Fases 1 (setup), 2 (design system), 3 (header e navegação), 4 (home),
5 (acomodações), 6 (institucional e localização), 7 (responsividade) e
8 (performance), 9 (SEO local) e 10 (QA) concluídas. **O MVP está pronto para
publicar.**

A home está completa: hero, apresentação, acomodações, comodidades, estrutura
em mosaico, Rio São Francisco, avaliações, chamada de WhatsApp e rodapé. O
rodapé é o mesmo nas quatro páginas.

`acomodacoes.html` está estruturada e sem nenhum dado inventado: as
categorias aparecem como estado vazio, e o modelo de card pronto para
preencher está em comentário no próprio HTML, logo acima. As regras da
hospedagem (check-in, check-out, pets, pagamento, cancelamento) são uma ficha
com todos os valores marcados como "a confirmar" — serve de checklist para a
conversa com o proprietário.

`pousada.html` traz a galeria das áreas comuns com as fotos atuais; a
história fica como estado vazio até a conversa com o proprietário.

`contato.html` tem a ficha de endereço, o mapa, o botão de rota, os canais de
contato e as perguntas frequentes.

O mapa do Google só é inserido **depois de um clique**: o iframe puxa 18
requisições de terceiros, e quem só quer o endereço ou a rota não paga por
isso. O espaço reservado tem a mesma altura do mapa, então não há salto de
layout na troca.

## Responsividade

A verificação é automatizada, não visual. `tools/auditoria-responsiva.py`
percorre as 4 páginas em 8 larguras
— 320, 375, 390, 430, 768, 1024, 1280 e 1440 px — e checa os critérios da
seção 19 do roadmap:

- rolagem horizontal real (`window.scrollX` depois de tentar rolar, não
  `scrollWidth`, que dá falso positivo com o menu offcanvas fechado);
- texto cortado por `overflow` escondido;
- alvos de toque abaixo de 44 px;
- imagens deformadas (proporção renderizada vs. natural, ignorando
  `object-fit`);
- texto abaixo de 12 px;
- botão flutuante de WhatsApp cobrindo conteúdo;
- linha de leitura acima de 85 caracteres, medindo o glifo "0" na fonte real
  do elemento (a Figtree tem "0" com 0,640em — estimar 0,5em inflava a conta
  em 28%).

Roda nos dois estados: com e sem número de WhatsApp confirmado.

```bash
python3 tools/servidor-local.py &
python3 tools/auditoria-responsiva.py        # estado atual
python3 tools/auditoria-responsiva.py --wa   # simulando WhatsApp confirmado
```

O script é ferramenta de desenvolvimento e não vai para o servidor — a pasta
`tools/` fica fora do deploy no Cloudflare Pages.

Além disso, o contraste do texto do hero é medido sobre os pixels compostos
da foto em 11 combinações de viewport, incluindo celular deitado e zoom de
200%. Pior caso atual: 4,96:1.

## Performance

Lighthouse rodado nas quatro páginas, servidas com compressão — como o
Cloudflare Pages faz. `tools/servidor-local.py` reproduz isso; o
`python3 -m http.server` não comprime e derruba a nota artificialmente.

| Página | Perf. mobile | Perf. desktop | Acess. | Boas práticas | SEO |
| ------ | ------------ | ------------- | ------ | ------------- | --- |
| index.html       | 98  | 99  | 100 | 100 | 100 |
| acomodacoes.html | 100 | 100 | 100 | 100 | 100 |
| pousada.html     | 100 | 100 | 100 | 100 | 100 |
| contato.html     | 100 | 100 | 100 | 100 | 100 |

Home no mobile: LCP 2,4 s · FCP 1,1 s · TBT 0 ms · CLS 0 · 289 KiB no total.
Nenhuma auditoria binária reprovada em nenhuma das quatro páginas.

O que trouxe o ganho:

- **Ícones em SVG inline** no lugar da fonte do Bootstrap Icons — eram 87 KB
  de CSS mais 134 KB de fonte para 21 símbolos.
- **`bootstrap.min.js` no lugar do bundle** — o bundle embute o Popper, usado
  só por dropdown, tooltip e popover. O site só usa o offcanvas.
- **Imagens recortadas na proporção de exibição.** O mosaico da home é 1:1 e a
  galeria é 4:3; antes o navegador baixava a foto vertical inteira para o
  `object-fit` descartar metade dos pixels.
- **`srcset` e `sizes` em todas as fotos**, com degraus de 300 a 1200 px.
- **Bootstrap e fonte no próprio domínio**, sem conexão a terceiros.

AVIF ficou de fora: o ambiente não tem codificador disponível. Vale gerar as
variantes AVIF junto com as fotos definitivas, quando houver ferramenta.

## SEO local

Cada página tem título único, meta description, canonical, Open Graph e
Twitter Card. `img/og-image.jpg` (1200×630) é a prévia que aparece quando o
link é compartilhado — importa porque o WhatsApp é o canal principal.

Dados estruturados em JSON-LD:

- `LodgingBusiness` na home e na página de contato;
- `BreadcrumbList` nas páginas internas;
- `FAQPage` na página de contato (as três respostas estão visíveis na página,
  como o Google exige).

### Buritizeiro e Pirapora

A pousada fica em **Buritizeiro** — esse é o endereço, no site e no schema.
Pirapora entra como segundo alvo geográfico: as duas cidades ficam em margens
opostas do Rio São Francisco, ligadas pela ponte, e quem procura hospedagem em
Pirapora tem na pousada uma opção do outro lado.

Como isso está implementado:

- `areaServed` no schema lista as duas cidades; `address` continua só
  Buritizeiro. Declarar endereço em Pirapora seria falsear a localização.
- Títulos e meta descriptions das quatro páginas citam as duas cidades.
- O conteúdo explica a relação geográfica onde ela ajuda quem lê — no
  cabeçalho da apresentação, na seção do rio e nas perguntas frequentes.
- A primeira pergunta frequente é literalmente "A pousada fica em Pirapora?",
  respondida com a verdade: não, fica em Buritizeiro, do outro lado da ponte.

Densidade dos nomes de cidade no texto visível: 2,2% a 3,7% por página,
somando as duas. Cheguei a repetir a ideia da ponte cinco vezes na home — já
lia como enchimento, e cortei para três.

**O schema só declara o que está confirmado.** Marcação estruturada com dado
errado é penalizada pelo Google, não apenas ignorada.

O bloco `LodgingBusiness` já traz `streetAddress`, `postalCode`, `telephone`,
`checkinTime`, `checkoutTime`, `petsAllowed`, `paymentAccepted` e `hasMap`.

Continuam fora, por dependerem de dado ainda não confirmado: `geo` (sem
coordenadas verificadas), `priceRange` e `aggregateRating`.

### Domínio

**Em uso:** `https://hotelpousadaquarios.paulodev.net`

Canonical, Open Graph e sitemap usam URL absoluta. Cheguei a deixar o
canonical relativo, para funcionar em qualquer domínio — o Google aceita. Mas
a auditoria de SEO do Lighthouse reprova (`Is not an absolute URL`) e
derrubava a nota de 100 para 92. Como o script de domínio já era obrigatório
por causa do Open Graph e do sitemap, absoluto saiu mais barato.

Para trocar (subdomínio novo, ou o domínio próprio da pousada):

```bash
python3 tools/definir-dominio.py https://outro.dominio.com.br
```

Atualiza as 29 URLs em HTML, `sitemap.xml` e `robots.txt`. O script descobre
o domínio atual lendo o canonical da home, então serve para trocar quantas
vezes precisar — não depende de haver um espaço reservado.

### Consistência de NAP

Nome, endereço e telefone precisam ficar idênticos entre site, Google
Business Profile e redes sociais:

```text
Hotel Pousada Aquários
Av. Barnabé Martins, 133 — Buritizeiro/MG, 39280-000
(31) 99520-6536
```

Conferir contra o perfil do Google está no checklist de `DEPLOY.md`.

## QA antes de publicar

```bash
python3 tools/servidor-local.py &
python3 tools/qa.py
```

Percorre as quatro páginas em **Chromium e Firefox** e verifica links
internos, âncoras, links externos, WhatsApp, mapa, menu, imagens, metadados,
dados estruturados, ordem de cabeçalhos e rolagem horizontal em oito
larguras. Qualquer `[FALHA]` impede a publicação; o domínio de espaço
reservado sai como `[aviso]`.

Última execução: **173 verificações, 0 falhas, 0 avisos.**

O passo a passo da publicação no Cloudflare Pages está em `DEPLOY.md`.

Falta apenas definir o domínio e conectar o repositório ao Cloudflare Pages —
o passo a passo está em `DEPLOY.md`.

O contraste do texto do hero é medido sobre os pixels compostos da foto, não
estimado — o pior caso em 11 tamanhos de viewport é 5.17:1, acima de AA. Se a
foto do hero for trocada, vale refazer essa medição.

Nenhum dado da pousada — WhatsApp, telefone, endereço, acomodações, preços,
políticas — foi confirmado com o proprietário. Nada disso deve ser publicado
como fato até a confirmação.
