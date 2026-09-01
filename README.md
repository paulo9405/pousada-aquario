# Hotel Pousada Aquários

Site institucional da Hotel Pousada Aquários — Buritizeiro/MG, às margens do
Rio São Francisco.

Site estático, sem backend. O objetivo é converter visitantes vindos do Google,
Instagram e indicações em contato direto pelo WhatsApp.

## Stack

HTML5 · CSS3 · Bootstrap 5.3.8 · Bootstrap Icons 1.13.1 · JavaScript vanilla ·
Cloudflare Pages

Bootstrap e Bootstrap Icons são carregados por CDN com Subresource Integrity.
A fonte (Figtree variável) é servida do próprio domínio, em `fonts/`.
Não há etapa de build: os arquivos são servidos como estão.

## Estrutura

```text
pousada-aquarios/
├── css/style.css        # design system completo
├── js/main.js           # configuração do site (contato, helpers)
├── fonts/               # Figtree variável (woff2, self-hosted)
├── img/                 # fotografias e logo (provisórias)
│   └── logo-nav.webp    # logo recortada e otimizada para o header
├── index.html           # Início
├── acomodacoes.html     # Acomodações
├── pousada.html         # A Pousada
├── contato.html         # Localização e contato
├── styleguide.html      # referência interna do design system (noindex)
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

## Status

Fases 1 (setup), 2 (design system) e 3 (header e navegação) concluídas.

O header é sticky, com navegação em offcanvas no mobile e barra horizontal a
partir de 992 px. As quatro páginas ainda mostram um placeholder no lugar do
conteúdo, que entra nas Fases 4 a 6.

Nenhum dado da pousada — WhatsApp, telefone, endereço, acomodações, preços,
políticas — foi confirmado com o proprietário. Nada disso deve ser publicado
como fato até a confirmação.
