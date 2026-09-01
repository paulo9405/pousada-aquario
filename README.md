# Hotel Pousada Aquários

Site institucional da Hotel Pousada Aquários — Buritizeiro/MG, às margens do
Rio São Francisco.

Site estático, sem backend. O objetivo é converter visitantes vindos do Google,
Instagram e indicações em contato direto pelo WhatsApp.

## Stack

HTML5 · CSS3 · Bootstrap 5.3.8 · Bootstrap Icons 1.13.1 · JavaScript vanilla ·
Cloudflare Pages

Bootstrap e Bootstrap Icons são carregados por CDN com Subresource Integrity.
Não há etapa de build: os arquivos são servidos como estão.

## Estrutura

```text
pousada-aquarios/
├── css/style.css        # tokens da identidade + base
├── js/main.js           # configuração do site (contato, helpers)
├── img/                 # fotografias e logo (provisórias)
├── index.html           # Início
├── acomodacoes.html     # Acomodações
├── pousada.html         # A Pousada
├── contato.html         # Localização e contato
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

## Identidade

As cores foram extraídas da logo e estão em `css/style.css` como tokens
`--aquarios-*`. Os contrastes foram verificados em WCAG 2.1 — as anotações
estão ao lado de cada token.

| Token                     | Valor     | Uso                              |
| ------------------------- | --------- | -------------------------------- |
| `--aquarios-primary`      | `#1A5FC2` | azul principal, links, botões    |
| `--aquarios-primary-dark` | `#0A2F63` | títulos, rodapé, overlays        |
| `--aquarios-primary-soft` | `#E8F0FB` | fundos de seção                  |
| `--aquarios-gold`         | `#F0C419` | destaque pontual (nunca dominante) |
| `--aquarios-text`         | `#17212E` | texto                            |

## Status

Fase 1 (setup inicial) concluída. As páginas exibem uma tela provisória de
verificação da base, que será substituída a partir da Fase 3.

Nenhum dado da pousada — WhatsApp, telefone, endereço, acomodações, preços,
políticas — foi confirmado com o proprietário. Nada disso deve ser publicado
como fato até a confirmação.
