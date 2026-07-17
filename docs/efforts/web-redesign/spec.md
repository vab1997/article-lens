---
title: 'Spec: rediseño de la web de ArticleLens (landing multi-sección EN/ES + privacy)'
label: ready-for-agent
status: open
created: 2026-07-17
map: map.md
---

# Spec: rediseño de la web de ArticleLens

> Producida por `/to-spec` desde el [mapa wayfinder](map.md) (6/6 decisiones cerradas el
> 2026-07-17). Los tokens exactos, la coreografía y los patrones CSS de referencia viven en las
> resoluciones de los tickets del mapa — este documento decide el QUÉ; los tickets guardan los
> valores.

## Problem Statement

La web actual de ArticleLens es una one-pager mínima de estética terminal (monospace, sin
animación, un screenshot estático) que no está a la altura del producto ni convierte: no cuenta
la historia local-first (el diferencial), no muestra el producto en acción, no existe en
español (el público hispano ya tiene la extensión localizada), y transmite "proyecto de fin de
semana" frente a referentes como Linear, Neon u OpenRouter. Quien llega desde el Chrome Web
Store o GitHub no encuentra razones visuales ni narrativas para instalar.

## Solution

Rediseño completo de `apps/web` con identidad propia ("Óptica": dark-only, Geist, acento
`#6ea8fe` — el mismo primary del side panel —, headlines two-tone, gradient borders con glow,
grain, profundidad sin sombras) y animación sutil (CSS-first + Motion vanilla, ~20 kB gzip):

- **Landing multi-sección** que cuenta la historia en orden: hero con un **demo animado del
  side panel resumiendo un artículo** (recreado en DOM, loop ~9 s, pausa en hover) → privacidad
  local-first con stat-row → cómo funciona (4 pasos) → "elige tu modelo" (3 caminos: on-device,
  free, tu key) → banda open source → CTA de cierre. Nav glass sticky y footer de columnas.
- **EN + ES** vía i18n nativo de Astro: un solo componente por página + diccionarios, `/es/`
  prefijado.
- **Privacy re-tokenizada**: misma estructura y contenido legal, nueva piel, hereda nav/footer,
  cero motion.

## User Stories

1. Como lector que llega desde el Chrome Web Store, quiero ver el side panel resumiendo un artículo real en el hero, para entender qué hace la extensión sin leer nada.
2. Como visitante escéptico de las herramientas de IA, quiero una sección de privacidad con números duros ("0 requests con tu texto", "100% en tu GPU"), para creer el claim local-first antes que un testimonial.
3. Como visitante nuevo, quiero un botón "Add to Chrome" visible en hero, nav y cierre, para instalar en el momento en que me convencí, sin buscar.
4. Como hispanohablante, quiero la landing completa en español bajo `/es/`, para evaluar el producto en mi idioma (la extensión ya me habla en español).
5. Como visitante en cualquiera de los dos idiomas, quiero un switch de idioma en la nav, para cambiar EN↔ES sin perder la página en la que estoy.
6. Como lector del demo del hero, quiero que el loop se pause cuando dejo el mouse encima, para poder leer el resumen generado a mi ritmo.
7. Como usuario con `prefers-reduced-motion`, quiero ver el estado final del demo estático y ninguna animación de entrada, para navegar sin movimiento.
8. Como visitante que scrollea, quiero que las secciones entren con reveals sutiles (fade + unos px, con stagger), para sentir el sitio cuidado sin que el movimiento distraiga.
9. Como visitante que quiere entender el flujo, quiero los 4 pasos (abrir panel, elegir modelo, resumir, exportar .md) numerados y en orden, para saber qué esperar tras instalar.
10. Como usuario sin GPU potente o sin ganas de descargar 2 GB, quiero ver en "elige tu modelo" que existen modelos cloud gratis (OpenRouter) con mi propia key, para saber que igual puedo usar la extensión gratis.
11. Como usuario avanzado, quiero ver que puedo traer mi key de OpenAI o Anthropic, para usar modelos frontier si los prefiero.
12. Como developer evaluando la herramienta, quiero una banda open source con link al repo, para auditar el código que va a leer mis artículos.
13. Como visitante desde mobile, quiero la landing completa y legible en una columna (el demo colapsa a panel solo), para evaluar desde el teléfono.
14. Como visitante que navega con teclado, quiero focus visible en links, botones y el switch de idioma, para operar el sitio sin mouse.
15. Como usuario existente con dudas legales, quiero la política de privacidad con la misma piel del sitio, nav y footer incluidos, para no sentir que salí a otra web.
16. Como lector de la política en español, quiero `/es/privacy` enlazada desde la landing ES y el footer, para leer lo legal en mi idioma.
17. Como visitante que comparte el sitio, quiero metadata OG/Twitter correcta por idioma y canonical por ruta, para que el link se vea bien al compartirlo.
18. Como visitante con conexión lenta, quiero que el JS de animación pese ~20 kB gzip y las fuentes ya estén self-hosted, para que el sitio abra rápido.
19. Como visitante en la nav, quiero anchors a Privacidad / Cómo funciona / Modelos, para saltar a la sección que me interesa en una página larga.
20. Como dueño del producto, quiero que el acento azul de la web sea el mismo primary del panel, para que web y extensión se reconozcan como el mismo producto.

## Implementation Decisions

- **Identidad "Óptica" (tokens en la resolución del ticket de dirección visual):** dark-only;
  Geist única familia (ya self-hosted vía fontsource; **el body deja `font-mono` y pasa a
  sans**, mono queda solo para métricas/números con `tabular-nums`); canvas `#0b0d0e` con
  escalera de superficies y hairlines en lugar de sombras; acento `#6ea8fe` con foreground
  `#0b1220` (par heredado del side panel); headlines two-tone (base gris + `<strong>` blanco);
  gradient borders con glow azul de esquina para el panel del hero y la card destacada; luz de
  esquina en cards; grain overlay (tile SVG con blend overlay); nav glass de 64 px con blur;
  radios 8/12/14 px. Los valores exactos NO se re-deciden al implementar: se copian del ticket.
- **Estructura de la landing (una página, secciones en este orden):** nav sticky glass (logo,
  anchors a Privacidad/Cómo funciona/Modelos, switch EN↔ES, CTA) → hero (eyebrow, H1 two-tone,
  sub, CTA primario "Add to Chrome" + secundario GitHub, demo animado) → privacidad (claim +
  stat-row de 4 números) → cómo funciona (4 pasos numerados) → elige tu modelo (3 cards:
  On-device destacada · Free cloud OpenRouter · Tu key OpenAI/Anthropic) → banda compacta open
  source → sección CTA de cierre → footer de columnas (producto / legal / idioma + marca).
  CTAs solo en hero, nav y cierre — nada inline entre secciones.
- **Demo del hero (coreografía completa en la resolución de su ticket):** ventana browser mock
  (dots + URL) con artículo a la izquierda y panel idealizado a la derecha; secuencia ~9 s
  (auto-click → progreso en dos fases → streaming de título y TL;DR por palabra con caret →
  3 puntos con stagger → métricas → hold → fade y loop); trigger on-load; hover pausa;
  reduced-motion muestra el estado final. En mobile la columna del artículo se oculta.
  DOM estático + timeline JS con Motion (`animate` sequences) y driver de typing propio.
- **Sistema de animación:** CSS-first. Micro-interactions en CSS puro (hover brightness,
  active scale). Reveals on-scroll: Motion `inView` togglea una clase; la animación (fade +
  translateY de pocos px) y el stagger viven en CSS. Tokens de motion como custom properties
  (velocidades + easings out-quad / out-expo). `prefers-reduced-motion: reduce` desactiva todo
  globalmente. Sin React, sin islands, sin GSAP: `motion` como única dependencia nueva de
  runtime, importada desde scripts vanilla procesados por Vite.
- **i18n:** config `i18n` nativa de Astro — `defaultLocale: 'en'`, locale `es` con prefijo
  `/es/`. Un componente de landing y uno de privacy renderizan ambos idiomas leyendo
  diccionarios TS compartidos (módulo puro, un objeto por locale con las mismas keys). El
  switch de idioma mapea la ruta actual a su equivalente en el otro locale. Las páginas ES
  declaran `lang="es"` y su OG locale; canonical por ruta como hoy.
- **Privacy:** re-tokenizar solamente — estructura de columna simple y contenido legal
  intactos (los textos ES existentes se mueven al diccionario). Hereda nav y footer nuevos; el
  link "← ArticleLens" desaparece. Cero motion (solo hover en links).
- **Se conserva:** Vercel Analytics, metadata/JSON-LD del layout (ajustada por locale), URLs de
  Chrome Web Store y GitHub, deploy Vercel con root `apps/web`.
- **Presupuesto de performance:** ~20 kB gzip de JS de animación total (medido en build); las
  imágenes nuevas que aparezcan van lazy salvo el demo (que es DOM, no imagen).

## Testing Decisions

- **Una costura unit-testeable: los diccionarios i18n.** Vitest en la app web (primera infra de
  tests ahí), siguiendo la convención de la extensión: carpeta `__tests__/` dentro del módulo,
  imports relativos. Tests de comportamiento externo, no de implementación: EN y ES exponen
  exactamente el mismo set de keys (deep-equal de shapes), ningún string vacío, y las rutas del
  switch de idioma mapean ida y vuelta. Prior art: los tests de entry-state y model-cache de la
  extensión (v13).
- **Todo lo demás no se unit-testea** (sería testear implementación de un sitio estático):
  `pnpm build:web` verifica que ambos locales compilan y emiten sus rutas; `pnpm lint:web`
  (ESLint + Prettier); QA visual en browser con checklist: coreografía completa del demo,
  hover-pausa, reveals on-scroll, reduced-motion (estado final estático, cero entradas),
  responsive (≤760 px: demo colapsa, stat-row 2 col, cards 1 col), navegación por teclado,
  ambos idiomas, Lighthouse como verificación del presupuesto de performance.

## Out of Scope

- Dominio custom (sigue `article-lens-web.vercel.app`).
- Cambios en `apps/extension`.
- Tema claro.
- Blog, changelog, testimonials, páginas nuevas más allá de landing + privacy.
- Screenshots o video reales del producto (el demo es DOM idealizado — decisión de mapa).

## Further Notes

- Prototipos aprobados (referencia visual vinculante para el implementador):
  [direcciones visuales](https://claude.ai/code/artifact/c6ec4da6-a612-4f7e-bd35-9f2b968a7af6)
  (ver dirección B) y
  [hero demo](https://claude.ai/code/artifact/730dfbde-47a9-4e09-bcdf-2f59bb484da2).
- Research de soporte en `assets/`: deconstrucción de referencias (patrones CSS con valores de
  producción) y stack de animación (números de bundle, sketch de integración en Astro).
- La lección editorial que gobierna todo el motion: **la sutileza se logra por omisión** —
  headings estáticos, sin parallax, sin scroll-jacking; el único espectáculo es el demo.
- Skills a consultar durante la implementación: `/emil-design-eng`, `/web-animation-design`,
  `/animation-vocabulary`.
