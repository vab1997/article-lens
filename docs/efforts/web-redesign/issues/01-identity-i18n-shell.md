# 01 — Identidad "Óptica" + shell i18n (tokens, nav, footer)

**What to build:** el andamiaje visual y de idioma sobre el que se monta todo el resto. Tras
este ticket, `apps/web` sirve EN en `/` y ES en `/es/` con la piel nueva aplicada al layout
(canvas, superficies, hairlines, acento azul, Geist como sans), una **nav glass sticky** y un
**footer de columnas** nuevos, y un switch de idioma que preserva la ruta. La home puede quedar
como un placeholder mínimo (un hero de texto sin demo) — las secciones llegan en el 02 —, pero
el chrome (nav + footer), los tokens y el ruteo bilingüe quedan funcionando de punta a punta.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] `global.css` define los tokens de la identidad B (paleta canvas/superficies/hairlines, ink muted/faint, acento `#6ea8fe` + foreground `#0b1220`, radios 8/12/14, tokens de motion) — valores exactos copiados de la resolución del ticket de dirección visual del mapa.
- [ ] El body deja `font-mono`; Geist queda como familia sans por defecto; mono (`tabular-nums`) reservado a métricas/números.
- [ ] Config `i18n` nativa de Astro: `defaultLocale: 'en'`, locale `es` con prefijo `/es/`; `/` sirve EN, `/es/` sirve ES.
- [ ] Diccionarios TS compartidos (un objeto por locale, mismas keys) como módulo puro; el layout y los componentes leen strings desde ahí (nada hardcodeado en el markup).
- [ ] Nav glass sticky nueva: logo, anchors (Privacidad / Cómo funciona / Modelos), switch EN↔ES, CTA "Add to Chrome". Blur + hairline inferior; 64 px.
- [ ] El switch de idioma mapea la ruta actual a su equivalente en el otro locale (ida y vuelta).
- [ ] Footer de columnas nuevo (producto / legal / idioma + marca), reemplaza el footer de una línea.
- [ ] Metadata del layout (title/description/OG/canonical/JSON-LD) ajustada por locale; `lang` y `og:locale` correctos en ES.
- [ ] `pnpm build:web` y `pnpm lint:web` pasan; ambas rutas emiten.
