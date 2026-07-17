# 03 — Sistema de animación (Motion + reveals CSS-first)

**What to build:** la capa de movimiento sutil sobre las secciones ya maquetadas. Instala
`motion` como única dependencia de runtime nueva y establece el patrón CSS-first: las secciones
entran on-scroll con un reveal (fade + translateY de pocos px) y stagger cuando corresponde, las
micro-interactions (hover, active) responden, y `prefers-reduced-motion` desactiva todo
globalmente. Tras este ticket la landing "se siente" viva al scrollear sin ningún espectáculo
(el demo del hero es aparte, ticket 04).

**Blocked by:** 02 — Secciones de la landing.

**Status:** ready-for-agent

- [ ] `motion` agregado a `apps/web`; importado desde un script vanilla procesado por Vite (sin React, sin islands).
- [ ] `inView` de Motion togglea una clase de reveal; la animación (fade + translateY pocos px) y el stagger viven en CSS con tokens de motion (easings out-quad / out-expo).
- [ ] Reveals aplicados a las secciones del cuerpo con stagger donde hay listas (stat-row, cards, pasos).
- [ ] Micro-interactions CSS: hover brightness en cards/links/botones, active scale en botones.
- [ ] `@media (prefers-reduced-motion: reduce)` desactiva reveals y transiciones globalmente (sin `!important`).
- [ ] Solo se animan `transform` y `opacity`; JS de animación dentro del presupuesto (~20 kB gzip, verificado en build).
- [ ] `pnpm build:web` y `pnpm lint:web` pasan.
