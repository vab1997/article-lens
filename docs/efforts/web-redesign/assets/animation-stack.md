# Research: stack de animación para la web (Astro 6, sin React)

> Ticket: [`../tickets/02-research-animation-stack.md`](../tickets/02-research-animation-stack.md) ·
> Fecha: 2026-07-17 · Estado de browsers verificado a mediados de 2026.

## Contexto real del proyecto

`apps/web` hoy: Astro 6.1.3 + Tailwind 4.2.2 (`@tailwindcss/vite`), adapter Vercel, Geist
variable, `@lucide/astro`. **Cero JS de UI**: no hay React, no hay islands, no hay `<script>`
de animación — solo 3 páginas `.astro` (index, privacy, es/privacy) y CSS global. Los
`<script>` dentro de `.astro` los procesa Vite (bundling + tree-shaking + TS), así que importar
una lib npm desde un script vanilla es un camino de primera clase en Astro — no requiere island.

Los tres targets de animación del mapa son de naturaleza distinta:

| Target | Naturaleza técnica |
| --- | --- |
| Entrance reveals on-scroll con stagger | **Trigger al entrar al viewport** (one-shot, time-based) — no scrub atado al scroll |
| Micro-interactions (hover, botones, links) | Transiciones CSS puras, 100–250 ms |
| Demo del hero (~5–10 s: typing, puntos, progreso) | **Secuencia coreografiada por tiempo** + loop, con estados DOM (texto que crece) |

Distinguir "reveal al entrar" de "animación scrubbed por scroll" es la clave de toda la
decisión: lo que hace Linear son reveals **time-based disparados por IntersectionObserver**
(ease-out ~0.5 s, stagger ~80–120 ms), no scrubbing.

---

## Opción 1 — CSS puro moderno

### `animation-timeline: scroll()` / `view()`

- **Chrome/Edge 115+, Safari 26 (sep 2025)**: soporte completo. **Firefox estable: NO** —
  sigue detrás del flag `layout.css.scroll-driven-animations.enabled` en Firefox 152 (jun
  2026); es prioridad Interop 2026 pero no shipped. Global ~82 %.
- Además, es la herramienta **equivocada** para reveals estilo Linear: `view()` ata el progreso
  de la animación a la posición de scroll (scrub, reversible), no dispara una animación
  temporal con easing propio. Sirve para parallax/progress bars, no para "entra y se asienta".
- Veredicto: no usar como base. Opcional como progressive enhancement puntual (p.ej. glow del
  hero que se desvanece al scrollear) detrás de `@supports (animation-timeline: view())`.

### `@starting-style` + transitions

- Chrome 117+, Firefox 129+, Safari 17.5+ — ~89 % global, utilizable. Pero solo cubre
  "elemento aparece en el DOM / cambia display"; los reveals on-scroll igual necesitan un
  IntersectionObserver que toggle una clase. Útil si el demo del hero inserta nodos (puntos
  que aparecen) y queremos su entrada en CSS puro.

### Qué alcanza CSS puro

- **Micro-interactions: 100 % CSS.** `transition` + `@media (hover: hover) and (pointer: fine)`.
- **Reveals con stagger: CSS al 90 %** — la animación y el stagger
  (`transition-delay: calc(var(--i) * 90ms)`) viven en CSS; falta solo el trigger (~15 líneas
  de IntersectionObserver o `inView` de Motion).
- **Secuencia del hero: NO.** Un guion de 5–10 s con typing carácter a carácter, puntos que
  aparecen a destiempo, barra de progreso y loop es inmantenible como pila de
  `animation-delay` encadenados (cualquier ajuste re-cronometra todo a mano) y el typing de
  texto multilínea con `steps()` es frágil.

---

## Opción 2 — Motion vanilla (`motion`, sin React) ⭐

El package `motion` funciona sin React (`import { animate, inView, scroll, stagger, press, hover } from 'motion'`)
y tree-shakea por función. Pesos oficiales (motion.dev, v12):

| Import | gzip | Notas |
| --- | --- | --- |
| `animate` **mini** (`motion/mini`) | **~2.3–2.5 kB** | WAAPI puro; sin sequences, sin transforms independientes |
| `animate` **hybrid** (`motion`) | **~18 kB** | **sequences tipo timeline** (`[[el, props, { at }], …]`), springs, stagger, valores arbitrarios |
| `inView` | **~0.5 kB** | wrapper de IntersectionObserver, callback enter/leave |
| `scroll` | ~5.2 kB | usa ScrollTimeline nativo cuando existe (no lo necesitamos) |
| `stagger` | ~0.1 kB | genera delays para reveals y sequences |

(El package completo mide 41 kB gzip en bundlephobia, pero eso es sin tree-shaking — con Vite
solo pagás lo que importás.)

- **Sequences** (solo hybrid): array de segmentos con `at` absoluto/relativo/labels — exactamente
  el DX que pide el hero. El typing lo escribís vos igual (ninguna lib lo trae), pero se
  orquesta dentro de la secuencia o con un mini-driver async.
- **Reduced motion**: sin helper vanilla — un check manual de
  `matchMedia('(prefers-reduced-motion: reduce)')` antes de arrancar (3 líneas) + media queries
  en el CSS de reveals.
- **Astro**: import directo en `<script>` de un `.astro`. Cero fricción.

## Opción 3 — GSAP + ScrollTrigger

- **Licencia: sí, 100 % gratis** desde abril 2025 (adquisición por Webflow), incluidos los
  ex-plugins de Club (SplitText, ScrollSmoother, etc.), con uso comercial. Verificado en
  gsap.com/pricing y webflow.com/updates.
- **Peso medido** (gsap 3.14.2): core **27.3 kB gzip** (70.5 kB min) + ScrollTrigger
  **17.9 kB gzip** (44.2 kB min) → **~45 kB gzip** el par. Solo timelines con el core ya son
  27 kB.
- DX excelente para timelines y scrubbing/pinning complejo, y funciona bien en `<script>` de
  Astro. Pero para "sutil nivel Linear" (reveals + una secuencia temporal, **sin** pinning ni
  scrub) es 2.2–2.5× el peso de Motion hybrid sin ganancia funcional. Descartado por
  presupuesto, no por calidad.

## Opción 4 — Astro nativo

- **`<ClientRouter />` / View Transitions**: solo aportan en navegación **entre páginas**
  (landing ↔ privacy). En una landing one-page no hacen nada, y meten JS de router. Si algún
  día se quiere el cross-fade landing→privacy, la vía barata es la CSS-only
  `@view-transition { navigation: auto }` (progressive enhancement, cero JS), no ClientRouter.
  **No usar ahora.**
- **`client:visible`**: es un modificador de **islands** (frameworks UI); no aplica a scripts
  vanilla. Irrelevante mientras no haya React.
- **`astro:page-load`**: solo existe con ClientRouter. Sin él, un `<script>` de módulo corre
  una vez al cargar — que es exactamente lo que queremos. Solo tener presente: si algún día se
  suma ClientRouter, los inits deben moverse a `astro:page-load`.

## ¿Isla React para el hero?

**No.** El demo es una secuencia coreografiada **sin estado interactivo del usuario** (no hay
inputs, no hay props reactivas): DOM estático en el `.astro` (fidelidad con el side panel real,
buen SSG/SEO) + un script que lo anima. Una isla React sumaría ~40+ kB de runtime para
renderizar HTML que ya podemos servir estático, y `motion` en modo React no agrega nada a la
coreografía que la API vanilla no tenga. React solo se justificaría si el demo se volviera
interactivo (elegir modelo, re-lanzar con input propio) — fuera de alcance del mapa.

---

## Matriz contra los criterios del ticket

| Criterio | CSS puro | Motion mini | **Motion hybrid (combo)** | GSAP+ST |
| --- | --- | --- | --- | --- |
| Peso JS total | 0 kB (pero no cubre el hero) | ~3 kB | **~19–20 kB** | ~45 kB |
| DX secuencias coreografiadas | ✗ inmantenible | ✗ sin sequences | ✓ sequences con `at`/labels | ✓✓ timelines |
| Scroll-reveals con stagger | ◐ falta trigger | ✓ inView+CSS | ✓ inView+CSS | ✓ (overkill) |
| `prefers-reduced-motion` | ✓ media query | ✓ MQ + 1 check JS | ✓ MQ + 1 check JS | ✓ `gsap.matchMedia` |
| Mantenibilidad en Astro estático | ✓✓ | ✓ | ✓ script vanilla, 0 islands | ✓ pero dependencia pesada |

## RECOMENDACIÓN

**Combo: CSS-first + Motion vanilla como única librería.**

1. **Micro-interactions → CSS puro** (transitions, `:active { scale: .97 }`, `@media (hover:hover)`). 0 kB.
2. **Reveals on-scroll con stagger → `inView` de Motion (~0.5 kB) + clases CSS.** La animación
   (opacity/translate, ease-out ~0.5 s) y el stagger (`--i` × 90 ms) viven en Tailwind/CSS; JS
   solo togglea `.is-visible` una vez. `prefers-reduced-motion` se resuelve en la media query.
   **No** usar `animation-timeline: view()` como base (Firefox estable sin soporte + semántica
   scrub ≠ reveal).
3. **Demo del hero → `animate` hybrid de Motion (~18 kB) con sequences** para la coreografía
   de ~5–10 s (entradas de puntos, progreso, cursor), más un mini-driver de typing propio
   (~30 líneas, `rAF`/async). Gate por reduced-motion: si `reduce`, mostrar el estado final
   estático del demo.
4. **Nada de ClientRouter/islands.** Si más adelante se quiere transición landing↔privacy:
   `@view-transition` CSS-only.

**Presupuesto resultante: ~19–20 kB gzip de JS de animación en toda la página** (hybrid
`animate` + `inView` + `stagger`, con overlap interno), vs ~45 kB de GSAP+ScrollTrigger para el
mismo resultado. Si durante el prototipo del hero (ticket 05) la secuencia resultara trivial
(solo typing + apariciones lineales), hay una salida de emergencia a `motion/mini` + CSS
(~3 kB), pero se pierde el DX de `at`/labels para re-cronometrar la coreografía — no vale la
pena a priori.

## Sketch de integración en Astro

```
apps/web/src/
  scripts/
    reveal.ts        # inView + toggle de clase
    hero-demo.ts     # coreografía del demo
  components/
    hero-demo.astro  # DOM estático del panel recreado + <script src>
```

```astro
---
// src/pages/index.astro (o el componente de sección)
---
<section data-reveal-group>
  <h2 data-reveal style="--i: 0">Local-first</h2>
  <p data-reveal style="--i: 1">…</p>
</section>

<script>
  import { inView } from 'motion'

  inView('[data-reveal-group]', (el) => {
    el.querySelectorAll('[data-reveal]').forEach((n) => n.classList.add('is-visible'))
  }, { amount: 0.3 })
</script>
```

```css
/* global.css — la animación y el stagger viven en CSS */
[data-reveal] {
  opacity: 0;
  translate: 0 16px;
  transition:
    opacity 0.5s cubic-bezier(0.215, 0.61, 0.355, 1),
    translate 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
  transition-delay: calc(var(--i, 0) * 90ms);
}
[data-reveal].is-visible { opacity: 1; translate: 0 0; }

@media (prefers-reduced-motion: reduce) {
  [data-reveal] { opacity: 1; translate: none; transition: none; }
}
```

```ts
// src/scripts/hero-demo.ts — esqueleto de la coreografía
import { animate, inView, stagger } from 'motion'

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches

export function initHeroDemo(root: HTMLElement) {
  if (reduced) return root.classList.add('demo-finished') // estado final estático

  inView(root, () => {
    run(root) // arranca solo cuando el hero es visible; loop con pausa entre ciclos
  }, { amount: 0.5 })
}

async function run(root: HTMLElement) {
  await typeText(root.querySelector('.demo-title')!, 'How WebGPU changes…') // driver propio
  await animate([
    ['.demo-progress', { width: ['0%', '100%'] }, { duration: 1.2 }],
    ['.demo-point', { opacity: [0, 1], y: [8, 0] }, { delay: stagger(0.35), at: '-0.4' }],
    ['.demo-badge', { scale: [0.9, 1], opacity: [0, 1] }, { at: '+0.2' }]
  ]).finished
}
```

El `<script>` va dentro del componente `.astro` (Vite lo bundlea y tree-shakea); corre una vez
por carga — correcto mientras no exista ClientRouter.

## Fuentes

- MDN — [CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) · [animation-timeline](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline)
- caniuse — [@starting-style](https://caniuse.com/mdn-css_at-rules_starting-style) (Chrome 117 / Firefox 129 / Safari 17.5, ~89 %)
- Mozilla Connect — [estado de animation-timeline en Firefox](https://connect.mozilla.org/t5/ideas/implement-css-scroll-driven-animations-animation-timeline/idi-p/116931) (flag en estable, Interop 2026)
- Motion — [quick start / mini vs hybrid](https://motion.dev/docs/quick-start) · [animate + sequences](https://motion.dev/docs/animate) · [inView](https://motion.dev/docs/inview) · [upgrade guide (scroll 5.2 kB)](https://motion.dev/docs/upgrade-guide)
- GSAP — [pricing: 100 % free](https://gsap.com/pricing/) · [Webflow: GSAP becomes free](https://webflow.com/updates/gsap-becomes-free)
- Medición propia (2026-07-17): bundlephobia API `gsap@3.14.2` = 27.3 kB gzip; `dist/ScrollTrigger.min.js` gzip = 17.9 kB; `motion@12.34.3` full = 41 kB gzip (sin tree-shaking)
- Astro — [View transitions](https://docs.astro.build/en/guides/view-transitions/) · [astro-transitions API](https://docs.astro.build/en/reference/modules/astro-transitions/)
