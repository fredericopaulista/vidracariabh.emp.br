import { defineConfig } from 'astro/config';

// Domínio de produção — usado para canonical, sitemap e URLs absolutas no schema.
export default defineConfig({
  site: 'https://vidracariabh.emp.br',
  trailingSlash: 'always',
});
