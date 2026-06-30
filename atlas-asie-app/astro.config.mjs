// @ts-check
import { defineConfig } from 'astro/config';

// Atlas Asie est servi sous hl-consulting.tech/atlas-asie (même montage que le hub).
// site + base pilotent la génération des liens/assets et des URLs canoniques.
export default defineConfig({
  site: 'https://hl-consulting.tech',
  base: '/atlas-asie',
  // Sortie 100% statique : on réplique le montage "dossier committé" du hub.
  output: 'static',
  trailingSlash: 'ignore',
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
    routing: {
      // FR par défaut, sans préfixe : /atlas-asie/ . EN sous /atlas-asie/en/.
      prefixDefaultLocale: false,
    },
  },
});
