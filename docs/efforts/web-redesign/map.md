---
label: wayfinder:map
status: closed
created: 2026-07-17
closed: 2026-07-17
---

# Mapa: Rediseño de la web (apps/web) — identidad nueva + animación sutil

## Destination

**`spec.md` lista para `/to-spec` → `/to-tickets` → `/implement`**: rediseño de la web de
ArticleLens — landing larga multi-sección (EN + ES) + restyle de `/privacy` y `/es/privacy` —
con la dirección visual, el sistema de animación y la arquitectura de contenido **ya decididos**.
El mapa termina cuando no queda ninguna decisión de diseño abierta antes de especificar.

## Notes

- Dominio: `apps/web` — Astro 6 + Tailwind v4, **sin React** hoy (islands permitidas si la
  decisión de stack de animación lo pide). Deploy Vercel (root dir `apps/web`).
- **Skills a consultar en cada sesión de este esfuerzo**: `/emil-design-eng` (taste y polish),
  `/web-animation-design` (easing/timing/performance), `/animation-vocabulary` (nombrar efectos).
- **Referencias**: [linear.app/homepage](https://linear.app/homepage) (la favorita),
  [neon.com](https://neon.com), [openrouter.ai](https://openrouter.ai). Se pueden mergear ideas
  de las tres y explorar otras opciones.
- Estética objetivo: **dark-only**, tipografía **Geist**, gradientes, glow, glass, animación
  **sutil**. `prefers-reduced-motion` obligatorio en todo lo animado.
- Instalar librerías de animación (motion, gsap) está permitido si hace falta.
- Preferencias del usuario: prototipos en código para reaccionar antes de cerrar decisiones
  visuales; presentar plan y esperar aprobación (memoria: plan-approval-before-implementing).

## Decisions so far

- (charting) **Destino = spec**, no ejecución: wayfinder resuelve decisiones; el build va por el
  pipeline estándar.
- (charting) **Alcance**: landing larga multi-sección + restyle de privacy (EN/ES). Landing
  **localizada EN + ES** (hoy solo EN).
- (charting) **Identidad nueva** — se abandona el estilo terminal/mono; Geist + gradientes +
  glow + glass; la dirección final se elige **reaccionando a 2–3 prototipos**.
- (charting) **Hero = demo animado recreado** del side panel (HTML/CSS animado: texto que se
  resume, puntos que aparecen) — no screenshot estático ni video.
- (charting) **Dark-only** (sin tema claro).
- (charting) **Historias de la landing**: local-first/privacidad (diferencial), modelos gratis
  OpenRouter, providers pagos (OpenAI/Anthropic), cómo funciona (4 pasos), open source.
- [Research: deconstruir las referencias (Linear, Neon, OpenRouter)](tickets/01-research-references.md) —
  12 patrones extraídos del CSS real de producción: Linear = profundidad sin sombras (surface
  ladder + hairlines + top-edge highlight), glass nav `blur(20px)`, grain overlay, entradas de
  4px con motion tokenizado; Neon = gradient borders con glow (`mask-composite: exclude`),
  headlines two-tone; OpenRouter = mesh/starfield CSS, entradas `spawn-*` con stagger 50ms.
  Ninguna depende de gsap. Sutileza = omisión.
  Detalle: [assets/references-deconstruction.md](assets/references-deconstruction.md).
- [Research: stack de animación para Astro sin React](tickets/02-research-animation-stack.md) —
  combo CSS-first + **Motion vanilla** (única lib, ~19–20 kB gzip): micro-interactions en CSS
  puro; reveals via `inView` (~0.5 kB) + clases CSS con stagger; demo del hero con `animate`
  hybrid (~18 kB) + sequences; sin React ni GSAP (~45 kB, descartado por peso).
  Detalle: [assets/animation-stack.md](assets/animation-stack.md).
- [Arquitectura de información de la landing](tickets/03-grilling-landing-ia.md) — orden: hero →
  privacidad (claim + stat-row) → cómo funciona (4 pasos) → modelos (UNA sección, 3 cards:
  on-device · free · pago) → banda open source → CTA final; nav sticky glass con anchors +
  idioma + CTA; CTAs solo hero/nav/cierre; footer de columnas livianas; ES via **i18n nativo de
  Astro** (un componente + dicts, `/es/` prefijado).
- [Dirección visual (prototipos)](tickets/04-prototype-visual-direction.md) — elegida **B
  "Óptica" con el azul de la extensión (`#6ea8fe`)**: canvas `#0b0d0e`, headlines two-tone,
  gradient borders con glow azul de esquina, grain overlay, nav glass 64px, sin drop-shadows;
  tokens completos (paleta/tipo/radios/motion) en la resolución del ticket. Prototipo:
  https://claude.ai/code/artifact/c6ec4da6-a612-4f7e-bd35-9f2b968a7af6
- [Hero: demo animado del side panel (prototipo)](tickets/05-prototype-hero-demo.md) —
  **browser + artículo** (mobile: panel solo), coreografía ~9 s en loop (click → progreso →
  streaming título/TL;DR → puntos stagger → métricas), hover = pausa, reduced-motion = estado
  final estático, fidelidad idealizada. Prototipo:
  https://claude.ai/code/artifact/730dfbde-47a9-4e09-bcdf-2f59bb484da2
- [Alcance del restyle de privacy](tickets/06-grilling-privacy-restyle.md) — re-tokenizar sobre
  la identidad B (estructura y contenido legal intactos), heredar nav glass + footer nuevos,
  cero motion (solo hover en links). **Destino alcanzado — no quedan decisiones abiertas; mapa
  cerrado, sigue `/to-spec`.**

## Not yet specified

- Copy definitivo EN + ES por sección — la IA ya está cerrada (secciones fijadas), pero el copy
  es trabajo de la spec, no una decisión de mapa: se redacta en `/to-spec`.
- Detalle del mapa de animaciones por sección (vocabulario ya fijado: reveals `inView` + clases
  CSS con stagger; demo del hero ya coreografiado en su ticket).
- Presupuesto de performance a validar en QA (el research de stack fijó ~19–20 kB gzip de JS de
  animación; Lighthouse como verificación de la spec).
- Assets: no hacen falta capturas (fidelidad del demo = idealizada, resuelto en el ticket 05).

Nada de lo anterior es una **decisión** pendiente — todo es trabajo de la spec (`/to-spec`).

## Out of scope

- **Dominio custom** — sigue article-lens-web.vercel.app; se resuelve en otro esfuerzo.
- **Cambios en la extensión** (`apps/extension`).
- **Tema claro.**

## Tickets

| Ticket | Tipo | Bloqueado por |
| --- | --- | --- |
| [Research: deconstruir las referencias (Linear, Neon, OpenRouter)](tickets/01-research-references.md) | research | **cerrado** |
| [Research: stack de animación para Astro sin React](tickets/02-research-animation-stack.md) | research | **cerrado** |
| [Arquitectura de información de la landing](tickets/03-grilling-landing-ia.md) | grilling | **cerrado** |
| [Dirección visual (prototipos)](tickets/04-prototype-visual-direction.md) | prototype | **cerrado** |
| [Hero: demo animado del side panel (prototipo)](tickets/05-prototype-hero-demo.md) | prototype | **cerrado** |
| [Alcance del restyle de privacy](tickets/06-grilling-privacy-restyle.md) | grilling | **cerrado** |
