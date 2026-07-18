# 05 — Privacy re-tokenizada (EN/ES)

**What to build:** aplicar la piel nueva a `/privacy` y `/es/privacy` sin tocar la estructura ni
el contenido legal. Las páginas pasan a usar los tokens de la identidad B, heredan la nav glass
y el footer de columnas nuevos (desaparece el link "← ArticleLens"), y su copy se mueve a los
diccionarios EN/ES. Cero motion: solo transiciones de hover en links.

**Blocked by:** 01 — Identidad "Óptica" + shell i18n.

**Status:** ready-for-agent

- [ ] `/privacy` (EN) y `/es/privacy` (ES) renderizan con los tokens de la identidad B (tipografía, colores, hairlines, acento azul en links).
- [ ] Estructura de columna simple y contenido legal intactos; los textos (incluidos los ES existentes) viven en los diccionarios.
- [ ] Heredan la nav glass y el footer de columnas; el link "← ArticleLens" se elimina.
- [ ] Cero animación de entrada; solo hover en links.
- [ ] Metadata/canonical/lang correctos por locale; enlazadas desde el footer en ambos idiomas.
- [ ] `pnpm build:web` y `pnpm lint:web` pasan.
