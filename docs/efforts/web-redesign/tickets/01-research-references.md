---
title: 'Research: deconstruir las referencias (Linear, Neon, OpenRouter)'
label: wayfinder:research
status: closed
assignee: research-subagent (session 2026-07-17)
closed: 2026-07-17
blocked-by: []
map: ../map.md
---

## Question

¿Qué patrones concretos y aplicables usan las tres referencias —
[linear.app/homepage](https://linear.app/homepage) (favorita del usuario),
[neon.com](https://neon.com), [openrouter.ai](https://openrouter.ai) — para lograr su nivel de
polish, y cuáles sirven para una landing de ArticleLens (dark, Geist, gradientes/glow/glass,
animación sutil)?

A extraer por sitio, con la mayor concreción posible (valores, técnicas CSS, no impresiones):

- **Hero**: layout, jerarquía tipográfica (tamaños/pesos/tracking), cómo presentan el producto
  (mock recreado vs screenshot), tratamiento de fondo (gradientes, grain, glow).
- **Ritmo de secciones**: cuántas, qué cuenta cada una, espaciado vertical, cómo alternan
  layouts (texto+visual, grids de cards, bento).
- **Técnicas de glass/glow/gradiente**: backdrop-filter, borders con gradiente, radial glows,
  máscaras, noise — cómo están construidas.
- **Animación**: qué anima on-scroll y qué on-load, vocabulario (fade-up, stagger, parallax…),
  duraciones/easings observables, qué NO anima (la sutileza es el punto).
- **Nav y footer**: sticky/glass nav, comportamiento al scrollear, densidad del footer.
- Qué librerías de animación se detectan en sus bundles (motion, gsap, CSS puro…).

Cierre: síntesis con los 5–10 patrones que valen la pena robar para ArticleLens y por qué.

Findings → `assets/references-deconstruction.md`.

## Resolution (2026-07-17)

Findings completos: [assets/references-deconstruction.md](../assets/references-deconstruction.md)
— basados en el CSS real de producción de los tres sitios (valores verificados, no impresiones);
incluye síntesis "Patrones a robar" con 12 patrones + anti-patrones.

- **Linear**: profundidad **sin sombras** — surface ladder (#010102 → #0f1011 → #141516…) +
  hairlines 1px + top-edge highlight; glass nav 64px (`blur(20px)` sobre `#0b0b0bcc`); grain
  como tile CSS 256px en `mix-blend-mode: overlay`; motion tokenizado (`--speed-quick .1s`,
  `--ease-out-quad`) con entradas de **solo 4px** de translateY; Motion (framer) presente pero
  quirúrgico — la base es CSS.
- **Neon**: técnica estrella = **gradient borders con glow localizado** (doble background
  `border-box` o pseudo + `mask-composite: exclude`); cards con "luz de esquina" (radial claro
  at 0 0 sobre linear diagonal); headlines two-tone (gris + `<strong>` blanco). Gap: cero
  `prefers-reduced-motion` (nosotros sí lo respetamos).
- **OpenRouter**: fondo mesh + starfield **100% CSS** (radiales sub-pixel); spotlight que sigue
  el cursor vía `--px/--py`; familia de entradas `spawn-*` (.25–.5s ease-out-expo, stagger 50ms
  por nth-child); stats vivos como social proof.
- **Cruza con el ticket 02**: ninguna de las tres depende de gsap — casi todo CSS puro + delays
  escalonados; confirma la viabilidad del stack CSS-first + Motion en Astro sin React.
- Síntesis mapeada a ArticleLens: side panel recreado como "surface 1" con hairline + fade-mask
  inferior; stat-row privacy-first ("0 requests con tu texto"); marquee de modelos con
  edge-masks. Lección central: **la sutileza se logra por omisión** (headings estáticos, sin
  parallax).
