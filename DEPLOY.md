# Publicação — Hotel Pousada Aquários

Site estático, sem etapa de build. O Cloudflare Pages serve os arquivos como
estão, direto do repositório.

## Antes de publicar

### 1. Definir o domínio

Canonical, Open Graph e sitemap usam URL absoluta e estão com o espaço
reservado `https://DOMINIO-A-DEFINIR`. Sem trocar, a prévia do link no
WhatsApp não carrega a imagem e o Search Console rejeita o sitemap.

```bash
python3 tools/definir-dominio.py https://seudominio.com.br
```

Se for publicar primeiro no endereço temporário do Cloudflare, use ele:

```bash
python3 tools/definir-dominio.py https://pousada-aquarios.pages.dev
```

E rode de novo quando o domínio definitivo entrar no ar.

### 2. Rodar o QA

```bash
python3 tools/servidor-local.py &
python3 tools/qa.py
```

Percorre as quatro páginas em Chromium e Firefox e verifica links, WhatsApp,
mapa, menu, imagens, metadados, dados estruturados, cabeçalhos e rolagem
horizontal em oito larguras. **Qualquer `[FALHA]` impede a publicação.**

O servidor local comprime texto como o Cloudflare faz — o
`python3 -m http.server` não comprime e derruba a nota do Lighthouse
artificialmente.

### 3. Rodar o Lighthouse

```bash
npx lighthouse http://127.0.0.1:8900/index.html --view
```

Referência atual (mobile, servido com compressão): Performance 98–100,
Acessibilidade 100, Boas Práticas 100, SEO 100.

## Publicar

1. No painel do Cloudflare: **Workers & Pages → Create → Pages → Connect to Git**
2. Escolha o repositório `paulo9405/pousada-aquario`
3. Configuração de build:

   | Campo | Valor |
   | ----- | ----- |
   | Framework preset | None |
   | Build command | *(deixar vazio)* |
   | Build output directory | `/` |

4. Deploy. O Cloudflare já serve HTTPS e compressão sem configuração extra.
5. O arquivo `_headers` na raiz define o cache: um ano para imagens, fontes e
   `vendor/`; revalidação a cada visita para o HTML.

## Domínio próprio

Em **Custom domains**, adicione o domínio e siga as instruções de DNS. Depois
que propagar, rode `tools/definir-dominio.py` com o domínio definitivo,
comite e faça push — o Cloudflare republica sozinho.

## Depois de publicar

- [ ] Abrir o site no celular de verdade e testar o botão do WhatsApp
- [ ] Compartilhar o link em uma conversa do WhatsApp e conferir se a imagem
      de prévia aparece
- [ ] Google Search Console: adicionar a propriedade e enviar
      `https://seudominio.com.br/sitemap.xml`
- [ ] Conferir que nome, endereço e telefone estão **idênticos** no site e no
      Google Business Profile:

      Hotel Pousada Aquários
      Av. Barnabé Martins, 133 — Buritizeiro/MG, 39280-000
      (31) 99520-6536

- [ ] Rodar o teste de resultados avançados do Google na página inicial e na
      de contato, para validar o `LodgingBusiness` e o `FAQPage`

## O que ainda falta confirmar com o proprietário

Estão marcados no código com `data-confirmar` — para listar:

```bash
grep -rn "data-confirmar" *.html
```

- e-mail oficial
- política de crianças, cancelamento e acessibilidade
- categorias de quarto: nome, capacidade, tipo de cama, comodidades, preços
- história da pousada
- nota e quantidade de avaliações do Google
- o restante da lista de comodidades, hoje vinda do material de divulgação

## Substituição das fotos

As imagens atuais são provisórias. Quando as definitivas chegarem, gere as
variantes responsivas na mesma nomenclatura (`-400`, `-600`, `-800`, `-1200`,
`-sq-*`, `-43-*`) e troque os arquivos. O layout não muda: a proporção está
no container, não no arquivo.

Vale gerar também versões AVIF nessa hora — ficaram de fora porque o ambiente
de desenvolvimento não tinha codificador.
