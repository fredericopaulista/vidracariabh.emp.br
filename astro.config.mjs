import { defineConfig } from 'astro/config';

// Domínio de produção — usado para canonical e URLs absolutas no schema.
// Sitemap: arquivo estático em public/sitemap.xml (atualizar ao adicionar páginas/artigos).
export default defineConfig({
  site: 'https://vidracariabh.emp.br',
  trailingSlash: 'always',
});
