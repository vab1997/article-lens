---
title: 'Arquitectura de información de la landing'
label: wayfinder:grilling
status: closed
assignee: victorbejas (session 2026-07-17)
closed: 2026-07-17
blocked-by: []
map: ../map.md
---

## Question

¿Cómo se estructura la landing multi-sección? A cerrar en conversación (`/grilling`):

- **Orden y contenido de secciones** a partir de las historias ya decididas: hero (demo animado),
  local-first/privacidad, modelos gratis OpenRouter, providers pagos (OpenAI/Anthropic), cómo
  funciona (4 pasos), open source, CTA final. ¿Cuáles se fusionan? (¿gratis + pago = una sección
  "elige tu modelo"?) ¿Qué layout le toca a cada una (texto+visual, grid, bento)?
- **Nav**: ¿hay navbar? ¿sticky/glass? ¿qué links (secciones ancla, GitHub, Chrome Web Store,
  privacy, switch de idioma)?
- **CTAs**: primaria (Add to Chrome) y secundaria (GitHub) — dónde se repiten a lo largo del
  scroll.
- **Footer**: densidad, links, idioma.
- **Routing ES**: estrategia en Astro para la landing localizada (`/es/`) — ¿i18n routing de
  Astro, duplicación de página con dict compartido, cómo se elige/cambia idioma?

Nota: el copy definitivo por sección NO se cierra acá (queda en la niebla hasta tener la IA);
acá se cierra la estructura.

## Resolution (2026-07-17)

Grillado en 2 rondas (todas las opciones recomendadas confirmadas por el usuario):

- **Orden de secciones**: 1. Hero + demo animado → 2. Local-first/privacidad ("nada sale de tu
  máquina" — el diferencial arriba) → 3. Cómo funciona (4 pasos) → 4. Modelos → 5. Open source →
  6. CTA final.
- **Modelos = UNA sección "elige tu modelo"** con los 3 caminos: on-device · free (OpenRouter) ·
  pago (OpenAI/Anthropic) — espeja el chooser real de la extensión v13.
- **Nav sticky glass** (estilo Linear, blur al scrollear): logo + links ancla a secciones
  (privacidad / cómo funciona / modelos) + switch de idioma + CTA "Add to Chrome".
- **Layouts: cada sección el suyo** — privacidad = claim grande + stat-row ("0 requests con tu
  texto"); cómo funciona = 4 pasos numerados con visual; modelos = 3 cards; **open source =
  banda compacta** (no sección completa) antes del cierre.
- **CTAs**: hero (primaria + GitHub secundaria) + nav persistente + sección de cierre. Sin CTAs
  inline entre secciones — sutileza por omisión.
- **Footer: columnas livianas** — 2–3 grupos: producto (Chrome Web Store, GitHub), legal
  (privacy EN/ES), idioma; cierre con marca.
- **Routing ES: i18n nativo de Astro** — config `i18n` (defaultLocale `en`, `/es/` prefijado),
  UN componente de landing + diccionarios compartidos (mismo espíritu que `locales/` en la
  extensión); privacy ES existente se alinea a este esquema.
