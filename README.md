# vidracariabh.emp.br

Site institucional da **Vidraçaria BH** — vidraçaria com atendimento em Belo Horizonte e
Região Metropolitana (Contagem, Betim, Nova Lima, Vespasiano, Lagoa Santa).

Build estático em [Astro](https://astro.build). Gerido pelo Link Flow
(`projetos/vidracaria-bh/projeto.md`, `plataforma: astro`).

## Estrutura

| Caminho | O quê |
|---|---|
| `src/pages/<slug>.astro` | Money Pages (geradas na Fase 3 do Link Flow) |
| `src/content/blog/<slug>.md` | Artigos do blog (content collection) |
| `src/layouts/BaseLayout.astro` | Shell HTML — `<head>`, meta, canonical, slot de JSON-LD |
| `src/layouts/MoneyPage.astro` | Molde das Money Pages (`molde_astro` no projeto.md) |

## Rodar

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # gera dist/
```

## Publicar

1. `draft: true` → `false` no frontmatter do que for ao ar.
2. `git push` para `origin/main`.
3. Deploy do `dist/` no host (fora do escopo do Link Flow).
