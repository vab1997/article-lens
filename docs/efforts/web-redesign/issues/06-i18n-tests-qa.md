# 06 — Tests de diccionarios i18n + QA de release

**What to build:** la red de seguridad y la verificación final. Introduce la primera infra de
tests en `apps/web` (Vitest) cubriendo la única costura unit-testeable — los diccionarios i18n —
y corre el QA visual end-to-end contra el checklist de la spec en ambos idiomas antes de dar el
rediseño por listo.

**Blocked by:** 02 — Secciones de la landing · 03 — Sistema de animación · 04 — Demo del hero ·
05 — Privacy re-tokenizada.

**Status:** ready-for-agent

- [ ] Vitest configurado en `apps/web` (convención de la extensión: `__tests__/` en el módulo, imports relativos, sin alias).
- [ ] Tests de los diccionarios: EN y ES exponen exactamente las mismas keys (deep-equal de shapes), ningún string vacío, y el mapeo de rutas del switch de idioma va y vuelve correctamente.
- [ ] `pnpm build:web` verifica que ambos locales compilan y emiten sus rutas (`/`, `/es/`, `/privacy`, `/es/privacy`).
- [ ] QA visual en browser (checklist de la spec): coreografía completa del demo + hover-pausa; reveals on-scroll; `prefers-reduced-motion` (estado final estático, cero entradas); responsive ≤760 px (demo colapsa, stat-row 2 col, cards 1 col, sin scroll horizontal); navegación por teclado con focus visible; ambos idiomas y el switch.
- [ ] Lighthouse como verificación del presupuesto de performance (JS de animación ~20 kB gzip).
- [ ] `pnpm lint:web` limpio.
