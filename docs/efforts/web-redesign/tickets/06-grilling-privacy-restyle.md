---
title: 'Alcance del restyle de privacy'
label: wayfinder:grilling
status: closed
assignee: victorbejas (session 2026-07-17)
closed: 2026-07-17
blocked-by: [04-prototype-visual-direction.md]
map: ../map.md
---

## Question

¿Cuánto se rediseñan `/privacy` y `/es/privacy` sobre la identidad nueva? A cerrar en
conversación, con la dirección visual ya elegida:

- ¿Solo re-tokenizar (tipografía/colores/espaciado de la identidad nueva sobre la estructura
  actual) o rediseño de layout (nav compartida, hero propio, TOC)?
- ¿Las páginas de privacy heredan la nav/footer nuevos de la landing?
- ¿Alguna animación (¿entrada sutil?) o cero motion en páginas legales?
- ¿El contenido legal queda intacto? (default: sí — solo presentación.)

Bloqueado por: [Dirección visual](04-prototype-visual-direction.md).

## Resolution (2026-07-17)

- **Re-tokenizar, no rediseñar**: `/privacy` y `/es/privacy` mantienen su estructura de columna
  simple; se aplican los tokens de la identidad B (Geist con la escala nueva, canvas/superficies,
  hairlines, acento azul en links). **Contenido legal intacto.**
- **Heredan nav glass y footer de columnas** de la landing — una sola familia visual; el link
  "← ArticleLens" actual desaparece.
- **Cero motion**: solo transiciones de hover en links. Sin entradas animadas.
- Las páginas se alinean además al esquema i18n nativo de Astro decidido en la IA de la landing.
