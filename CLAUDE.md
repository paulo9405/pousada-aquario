# Hotel Pousada Aquários

Site institucional estático. Sem etapa de build.

## Leia antes de alterar

**[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** — memória técnica e de produto do
projeto: contexto comercial, estratégia geográfica Buritizeiro/Pirapora,
identidade visual com os valores exatos, o que é dado confirmado e o que é
provisório, e as armadilhas já pagas.

**[DEPLOY.md](DEPLOY.md)** — publicação no Cloudflare Pages.

## Regras que não mudam

1. **Não execute `git commit` nem `git push`.** Os commits são feitos
   manualmente pelo proprietário do projeto. Ao concluir, informe os arquivos
   para o stage, a mensagem em Conventional Commits e os comandos.
2. **Não invente dado da pousada.** Categorias de quarto, preços, políticas,
   avaliações e comodidades dependem de confirmação com o proprietário. O que
   está pendente é marcado com `data-confirmar` no HTML.
3. **Não declare endereço em Pirapora** no Schema.org. A pousada fica em
   Buritizeiro; Pirapora entra como `areaServed`.

## Comandos

```bash
python3 tools/servidor-local.py   # http://127.0.0.1:8900 — imita o Cloudflare
python3 tools/qa.py               # 195 verificações, Chromium + Firefox
```

Não abra os arquivos com duplo clique: os links são absolutos a partir da raiz
e quebram no `file://`.

Rode `tools/qa.py` antes de qualquer publicação. Qualquer `[FALHA]` impede.
