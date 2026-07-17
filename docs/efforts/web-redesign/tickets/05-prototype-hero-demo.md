---
title: 'Hero: demo animado del side panel (prototipo)'
label: wayfinder:prototype
status: closed
assignee: victorbejas (session 2026-07-17)
closed: 2026-07-17
blocked-by: [02-research-animation-stack.md, 04-prototype-visual-direction.md]
map: ../map.md
---

## Question

¿Cómo es exactamente el demo animado del hero? Decidido: recreación del side panel en HTML/CSS
(no screenshot ni video), animada. Abierto — a decidir sobre un prototipo funcional:

- **Coreografía**: ¿qué secuencia cuenta mejor el producto en ~5–10 s? (¿artículo → click →
  streaming del TL;DR → puntos que aparecen con stagger → badge de métricas?) ¿loop o una sola
  pasada? ¿pausa en hover?
- **Fidelidad**: ¿réplica fiel del panel real (capturas como referencia) o versión idealizada/
  simplificada que lea mejor a tamaño hero?
- **Contexto**: ¿el panel solo, o browser mock con el artículo al lado (mostrando el "side
  panel junto a la página")?
- **Trigger**: ¿arranca on-load, on-view, on-scroll?
- Degradación con `prefers-reduced-motion` (¿estado final estático?).

Construir con el stack elegido en el research de animación y la dirección visual ya fijada;
consultar `/web-animation-design` para timing/easing. El usuario reacciona (HITL); la resolución
fija la coreografía y el approach técnico para la spec.

Bloqueado por: [Research: stack de animación](02-research-animation-stack.md) y
[Dirección visual](04-prototype-visual-direction.md).

## Resolution (2026-07-17)

Prototipo funcional (tokens B, coreografía completa):
https://claude.ai/code/artifact/730dfbde-47a9-4e09-bcdf-2f59bb484da2 — las tres decisiones
confirmadas por el usuario:

- **Contexto: browser + artículo.** Ventana mock (dots + URL bar) con el artículo a la
  izquierda y el panel a la derecha (split ~1.15fr/1fr, ancho hero ~900px) — cuenta "side panel
  junto a la página" sin palabras. En **mobile colapsa a panel solo** (la columna artículo se
  oculta). Ventana con gradient border azul de esquina + mask de fade inferior (fusión con el
  canvas, patrón Linear).
- **Coreografía (~9 s, loop infinito, trigger on-load):**
  1. reposo 0.9 s → botón "Summarize" se auto-presiona (scale .97, 180 ms)
  2. status "Reading article…" (spinner + barra 28%) 0.85 s
  3. "Summarizing on your GPU…" (barra 72% → 100%) ~1.2 s
  4. título streamea por palabra (70 ms/palabra) con caret azul parpadeante
  5. TL;DR streamea por palabra (55 ms/palabra)
  6. 3 puntos fade-up con stagger 160 ms
  7. métricas (`12.4s · 342 tokens · $0.00`, mono) pop con stagger 90 ms
  8. hold 3.2 s → fade-out 260 ms → reset → fade-in → loop.
  **Hover sobre el stage = pausa** (deja leer; al salir continúa).
  **`prefers-reduced-motion`: sin loop — estado final estático.**
- **Fidelidad: idealizada.** Header (dot verde + nombre + chip "Llama 3.2 3B · local") +
  botón + resultado + métricas. Sin selector de modelo ni export — marketing, no captura.
- Técnica para la spec: DOM estático + timeline JS (en producción: Motion `animate` sequences
  para la coreografía; streaming de texto = spans por palabra con reveal, driver propio).
