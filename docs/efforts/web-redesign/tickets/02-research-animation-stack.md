---
title: 'Research: stack de animación para Astro sin React'
label: wayfinder:research
status: closed
assignee: research-subagent (session 2026-07-17)
closed: 2026-07-17
blocked-by: []
map: ../map.md
---

## Question

¿Con qué stack técnico conviene animar la web (`apps/web`, Astro 6 + Tailwind v4, **sin React**)
para lograr animaciones sutiles nivel Linear — entrance reveals on-scroll, stagger, micro
interactions, el demo animado del hero — al menor costo de bundle y complejidad?

Opciones a comparar (instalar librerías está permitido):

- **CSS puro + `animation-timeline: scroll()`/`view()`** y `@starting-style` — soporte de
  browsers hoy, qué alcanza y qué no.
- **Motion (ex Framer Motion) vanilla** (`motion` package, sin React): API `animate`/`inView`/
  `scroll`, peso real (~kB gzip por feature), cómo se integra en `<script>` de Astro.
- **GSAP + ScrollTrigger**: peso, licencia actual (¿ya 100% gratis?), DX en Astro.
- **Astro nativo**: View Transitions / `client:visible` islands — ¿aportan algo aquí?
- ¿Hace falta sumar una isla React para algo, o vanilla cubre todo (incluido el demo del hero,
  que es una secuencia coreografiada: typing, aparición de puntos, progreso)?

Criterios: peso JS total, DX para secuencias coreografiadas, scroll-reveals con stagger,
`prefers-reduced-motion` fácil de respetar, mantenibilidad en un sitio Astro estático.

Cierre: recomendación única (o combo, p.ej. CSS para reveals + lib para el hero) con números.

Findings → `assets/animation-stack.md`.

## Resolution (2026-07-17)

Findings completos: [assets/animation-stack.md](../assets/animation-stack.md)

**Recomendación: combo CSS-first + Motion vanilla (una sola lib, ~19–20 kB gzip total).**

- **Micro-interactions → CSS puro** (0 kB, transiciones 100–250 ms).
- **Reveals on-scroll con stagger → `inView` de Motion (~0.5 kB gzip) + clases CSS**: la
  animación y el stagger (`--i` × ~90 ms) viven en CSS; JS solo togglea la clase;
  `prefers-reduced-motion` se resuelve en la media query. Clave conceptual: lo de Linear son
  reveals **time-based disparados por IntersectionObserver**, no scrubbing —
  `animation-timeline: view()` descartado como base (Firefox estable aún sin soporte, semántica
  scrub).
- **Demo del hero → `animate` hybrid de Motion (~18 kB gzip) con sequences** (`at`/labels — DX
  exacto para coreografía de 5–10 s) + driver de typing propio (~30 líneas). Con `reduce`:
  estado final estático.
- **Sin isla React ni ClientRouter** — DOM estático en `.astro` + script vanilla (Vite procesa
  `<script>` con imports npm de primera clase). React sumaría ~40 kB para nada.
- GSAP descartado por peso (~45 kB gzip core+ScrollTrigger medidos), no por licencia (100%
  gratis desde abril 2025). `@starting-style` utilizable (~89%) pero no cubre los targets.
- Escape hatch: `motion/mini` (~2.3 kB) si el prototipo del hero (ticket 05) resulta trivial.

El asset incluye matriz contra los 5 criterios, sketch de integración en Astro
(`src/scripts/` + snippet `.astro` + esqueleto de coreografía) y fuentes.
