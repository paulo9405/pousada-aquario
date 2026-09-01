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

O número oficial ainda não foi confirmado, então `AQUARIOS.whatsapp` está
vazio em `js/main.js`. Enquanto estiver assim:

- o botão flutuante de WhatsApp fica oculto;
- o botão "Reservar" do header leva para `contato.html`.

Ao preencher o número (só dígitos, com DDI e DDD), `initWhatsApp()` ativa
sozinho todos os pontos marcados com `data-whatsapp`: ajusta o `href` para
`wa.me` com a mensagem pré-preenchida e revela o botão flutuante. Nenhuma
outra alteração é necessária.

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
8 (performance) e 9 (SEO local) concluídas — as quatro páginas do MVP estão
construídas, auditadas e medidas.

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

`contato.html` tem a ficha de endereço, a área reservada do mapa e os canais
de contato. O snippet do iframe do Google Maps está em comentário no HTML,
pronto para colar quando o endereço for confirmado — vale carregá-lo só após
um clique, para não pesar no Lighthouse.

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

**O schema só declara o que está confirmado.** Nome, descrição, cidade,
estado, país e área atendida entram; rua, telefone, faixa de preço e nota de
avaliação ficam de fora até a validação com o proprietário. Marcação
estruturada com dado errado é penalizada pelo Google, não só ignorada.

Quando os dados forem confirmados, acrescentar ao bloco `LodgingBusiness`:
`streetAddress`, `postalCode`, `telephone`, `geo`, `openingHoursSpecification`,
`priceRange` e — se a pousada quiser exibir a nota — `aggregateRating` com o
valor real.

### Antes de publicar: definir o domínio

Canonical, Open Graph e sitemap usam URL absoluta, com o espaço reservado
`https://DOMINIO-A-DEFINIR`.

Cheguei a deixar o canonical relativo, para funcionar tanto no endereço
temporário do Cloudflare quanto no definitivo — o Google aceita. Mas a
auditoria de SEO do Lighthouse reprova (`Is not an absolute URL`) e derrubava
a nota de 100 para 92. Como o script de domínio já era obrigatório por causa
do Open Graph e do sitemap, absoluto saiu mais barato.

```bash
python3 tools/definir-dominio.py https://seudominio.com.br
```

Troca as 29 ocorrências em HTML, `sitemap.xml` e `robots.txt` de uma vez. Sem
isso, a prévia do link no WhatsApp não carrega a imagem e o Search Console
rejeita o sitemap.

### Consistência de NAP

Nome, endereço e telefone precisam ficar idênticos entre site, Google
Business Profile e redes sociais. Como endereço e telefone ainda não foram
confirmados, essa checagem fica para a Fase 10.

Próxima fase: 10 (QA e deploy).

O contraste do texto do hero é medido sobre os pixels compostos da foto, não
estimado — o pior caso em 11 tamanhos de viewport é 5.17:1, acima de AA. Se a
foto do hero for trocada, vale refazer essa medição.

Nenhum dado da pousada — WhatsApp, telefone, endereço, acomodações, preços,
políticas — foi confirmado com o proprietário. Nada disso deve ser publicado
como fato até a confirmação.
