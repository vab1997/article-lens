# Deconstrucción de referencias: Linear, Neon, OpenRouter

> Ticket: [`01-research-references.md`](../tickets/01-research-references.md) · Fecha: 2026-07-17
>
> **Metodología**: fetch del contenido renderizado de cada sitio + descarga y análisis del CSS
> real de producción (los tres son Next.js; se bajaron todos los stylesheets y se greparon
> técnicas y valores). Complemento: el design-token teardown de linear.app en
> [awesome-design-md](https://github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md)
> (tercero, verificado contra el CSS real donde fue posible) y la serie
> [rebuilding-linear.app de frontend.fyi](https://github.com/frontendfyi/rebuilding-linear.app).
> Todos los valores CSS citados abajo salen del CSS de producción salvo que se indique lo contrario.

---

## 1. Linear (linear.app/homepage) — la favorita

### 1.1 Hero

- **Copy**: H1 "The product development system for teams and agents"; subhead 1 línea
  ("Purpose-built for planning and building products. Designed for the AI era."). Dos CTAs.
- **Jerarquía tipográfica** (tokens del teardown, consistentes con el CSS real):
  - `display-xl` ≈ **80px / weight 600 / line-height 1.05 / tracking ≈ -0.04em** (-3px a 80px).
    En el CSS real el título del hero colapsa a `font-size:38px !important` a ≤640px.
  - Tracking em-based observado en el CSS: `-.022em` en headings, `-.012em`/`-.015em` en
    intermedios, tendiendo a 0 en body. **Tracking negativo agresivo solo en display; el
    eyebrow usa tracking positivo (+0.4px)** para contrastar.
  - Fuente: **Inter Variable** (fallback SF Pro), con `font-feature-settings: "cv01","ss03"`
    (la "a" y dígitos alternativos — detalle que hace que Inter parezca custom).
    Mono: **Berkeley Mono**. Serif editorial: Tiempos Headline (solo en piezas editoriales).
  - Subhead: 18px / 400 / lh 1.5 (`body-lg`).
- **Presentación del producto**: **screenshots reales del producto a full-width** (imágenes
  1920×1080 servidas por Cloudflare Images, `loading="lazy"`), no video ni mock DOM en la home
  actual. La filosofía documentada: *"product UI screenshots as the protagonist of every
  section"* — el chrome de marketing es mínimo.
- **Fondo**: canvas casi negro **`#010102` / `#08090a`** ("faint blue tint is intentional" —
  nunca `#000` puro). En la iteración actual Linear **evita gradientes atmosféricos** (es un
  "don't" explícito de su sistema); el famoso glow del rebrand 2023 hoy está reducido a glows
  blancos casi subliminales (ver 1.3).

### 1.2 Ritmo de secciones

~12 secciones, historia lineal "del intake al monitoreo":

1. Hero (texto centrado + CTAs) → 2. Screenshots del producto full-width →
3. **3 columnas de value props** (texto corto) → 4–8. **Cinco feature blocks numerados**
(Intake 1.0, Plan 2.0, Build 3.0, Diffs 4.0, Monitor 5.0), todos con el mismo layout
**texto-izquierda / visual-derecha** (la repetición ES el ritmo; el visual cambia: lista de
issues, timeline gantt, terminal de agente, diff de código, dashboard) → 9. Changelog (stack
vertical de cards) → 10. Testimonials (carousel de 3 quotes) → 11. Statement de escala
("33,000+ product teams") → 12. CTA final centrado.

- **Espaciado**: secciones separadas por **96px**; `--page-padding-block: 64px`,
  `--page-padding-inline: 24px`; contenedor `max-width ≈ 1280px` centrado.
- Grid de cards 3-up → 2-up (1024px) → 1-up (768px). Radios: 8px botones/inputs, 12px cards,
  16px paneles de screenshot, 24px banners CTA.

### 1.3 Glass / glow / gradiente — cómo está construido

- **Profundidad sin sombras**: **no usan drop-shadows**. Jerarquía por "surface ladder" de
  4 escalones (`#0f1011 → #141516 → #18191a → #191a1b`) + **hairlines de 1px**
  (`#23252a`, `#34343a`) + un **highlight blanco sutil en el borde superior** de los paneles
  elevados (efecto emboss de 1px).
- **Glass del header**: `--header-bg: #0b0b0bcc` (negro al 80%) +
  `backdrop-filter: blur(var(--header-blur))` con `--header-blur: 20px`, borde inferior
  `#ffffff14`. Otros blurs en uso: 8px (tooltips/popovers), 4px, 24px, 32px, y un caso de
  `backdrop-filter: saturate(1.8) blur(20px)` (glass "juicy" estilo Apple).
- **Grain**: overlay dedicado —
  `.grain { position:absolute; inset:0; pointer-events:none; mix-blend-mode:overlay; opacity:.9; background-size:256px 256px; border-radius:inherit }`
  con variante `grainSubtle` a `opacity:.6`. Un tile de ruido de 256px repetido + blend
  overlay: mata el banding de los gradientes y da textura "cara" con costo casi nulo.
- **Glows**: casi subliminales —
  `radial-gradient(circle, rgba(255,255,255, var(--glow-opacity)) 0%, transparent 50%)` con
  `--glow-opacity: .03–.04`. Blanco al 3–4%, no color.
- **Shine beam que sigue el mouse** (cards interactivas): máscara elíptica posicionada con
  variables actualizadas por JS —
  `radial-gradient(ellipse var(--shine-beam-length) ... at var(--mask-x) var(--mask-y), #000 0%, #0009 30%, #0003 50%, #0000 70%)`
  con `--shine-beam-length: 200px`.
- **Masks por todos lados** (95 `mask-image` en el CSS): fade-out inferior de screenshots
  (`mask-image: linear-gradient(to bottom, visible 0%, visible 40–80%, invisible 100%)`) para
  fundir el producto con el canvas, y edge-fades laterales de marquees
  (`invisible 0px → visible 80px → visible calc(100% - 80px) → invisible`).
- **Color**: un único acento cromático, lavanda `#5e6ad2` (hover `#828fff`), reservado a brand
  mark / CTA primario / focus / links. Verde `#27a644` como único semántico. "Don'ts"
  explícitos del sistema: no usar el acento como fondo, no introducir un segundo acento, no
  pill-rounding en CTAs, no light mode.

### 1.4 Animación

- **Sistema de tokens de motion** en CSS custom properties: velocidades
  `--speed-quickTransition: .1s`, `--speed-regularTransition: .25s`; y la **escala Penner
  completa de easings** como variables (`--ease-out-quad: cubic-bezier(.25,.46,.45,.94)` es el
  workhorse; también out-quart `(.165,.84,.44,1)`, out-expo `(.19,1,.22,1)`, out-quint, etc.).
- **Micro-interacciones, no espectáculo**: el patrón dominante es
  `transition: filter .16s var(--ease-out-quad)` + `:hover { filter: brightness(1.3) }` —
  hover = brillo, 160ms, ease-out. Nada de scale/bounce en la landing.
- **Keyframes reales**: `staggerIn { from { opacity:0; transform:translateY(4px) } }` —
  **¡solo 4px de desplazamiento!** La entrada es casi imperceptible, puro fade con un susurro
  de movimiento. `shimmerSweep` (sweep de `background-position` 150%→-50%), `cursorBlink`,
  `revealDots`, marquee `scroll { to { transform:translateX(calc(-100% - var(--Marquee-gap))) } }`
  linear infinito, y el set Radix de dialogs/tooltips (fadeIn/scaleIn, `dialogBounce`).
- **On-load vs on-scroll**: hero con fade/stagger sutil on-load; los feature blocks entran con
  el mismo vocabulario al scrollear. **No hay parallax, no hay scroll-jacking, los headings no
  animan.** Los screenshots son estáticos.
- **`prefers-reduced-motion: reduce` → `animation: none`** en los stagger items y en View
  Transitions (12 bloques en el CSS). Usan la **View Transitions API** para navegación.
- **Librería**: Next.js + CSS Modules para casi todo; en los chunks aparecen
  `use-motion-value`, `useReducedMotion` → **Motion (framer-motion) presente pero usado
  quirúrgicamente**, no como base del sistema. La base es CSS.

### 1.5 Nav y footer

- **Nav**: fija, **64px** de alto, glass (ver 1.3), links `body-sm` 14px. Densidad media:
  2 dropdowns + 5 links + login/signup.
- **Footer**: 5 columnas (~35 links), fondo canvas plano, texto `caption` 12px en
  `#8a8f98`, padding 64px/32px. Denso pero silencioso.

---

## 2. Neon (neon.com)

### 2.1 Hero

- H1: "Neon is the Postgres backend designed for apps and agents" —
  **`text-[72px] tracking-tighter leading-dense`**, colapsando 72→64→52→42→32px por
  breakpoint. Peso moderado (no black): la jerarquía se hace con **color, no con peso** (ver
  2.3). Dos CTAs ("Get started" / "Read the docs").
- **Presentación del producto**: carousel de 5 estados (Postgres, Auth, Functions, Storage,
  AI Gateway) con imágenes de producto + tagline; además **5 `<video>` autoplay** en feature
  sections (demos en video, no DOM recreado).
- **Fondo**: capas de patterns SVG responsivos + **overlays de noise como imagen**
  (`noise.jpg` a q=100 y `noise-background.svg`) — a diferencia de Linear (tile CSS), Neon
  sirve el grano como asset fotográfico grande.
- Fuentes: **esbuild** (display custom), IBM Plex Sans, **GeistMono** para código.

### 2.2 Ritmo de secciones

~12: banner de anuncio → hero carousel → "Cloud primitives" (CLI `npx neon init` como visual)
→ Autoscaling (split con **toggle de 2 estados** — sección interactiva) → Branching (grid de
3 cards) → Auth (tratamiento mínimo: icono + headline) → "No platform fees" (grid de 6 iconos)
→ "Backed by giants" (2 stats gigantes) → testimonial único → CTA final con comando copiable →
footer muy denso (compliance incluida). Alterna: split texto+visual / grid de cards / grid de
iconos / stats / quote — **cada sección cambia de layout** (lo opuesto al ritmo repetitivo de
Linear).

### 2.3 Glass / glow / gradiente — cómo está construido

- **Headline two-tone** (técnica firma): los H2 van en gris
  (`text-gray-new-50`) **con los `<strong>` en blanco** — jerarquía dentro del propio titular
  sin tocar tamaño ni peso. Barato y elegantísimo.
- **Bordes con gradiente + glow localizado** (técnica estrella, 2 variantes en el CSS):
  1. Doble background clipeado al borde:
     `background: radial-gradient(35% 50% at 0 0, #387667cc, transparent) border-box, linear-gradient(#242628, #242628) border-box`
     — el borde de la card es gris neutro pero con un **halo de color (verde/azul) entrando por
     una esquina**.
  2. Pseudo-elemento + doble máscara compuesta:
     `mask-image: linear-gradient(#fff 0 0), linear-gradient(#fff 0 0)` con
     **`mask-composite: exclude` (7 usos) / `xor` (21 usos)** — deja visible solo el anillo del
     borde para pintarlo con cualquier gradiente.
- **Card backgrounds con "luz de esquina"**:
  `background: radial-gradient(100% 127% at 0 0, #30323666 0%, transparent 49%), linear-gradient(165deg, #161718, #0c0d0e)`
  — un radial claro anclado en la esquina superior izquierda sobre un linear oscuro diagonal.
  Repiten el patrón con tintes de color (`#153737` teal, `#233632`).
- **Glow del acento**: verde brand `#00e599` en radiales de baja alfa
  (`radial-gradient(50% 50% at 50% 100%, #00e59926, transparent)` — 15% alpha desde el borde
  inferior).
- **Spotlight masks**: `mask-image: radial-gradient(350px at 50% -200px, #000 25%, transparent 100%)`
  — revelan un pattern/grid **solo alrededor de un punto**, el resto se funde a negro.
- Backdrop-filter: poco (14 usos, mayormente utilidades Tailwind) — Neon es más "gradiente y
  máscara" que "glass".

### 2.4 Animación

- **CSS puro, poquísimo JS de animación**: `shimmer` (translate 100%, 2s infinite),
  `infinityScroll` **60s linear infinite** (marquee de logos con `--gap` responsivo),
  `logoMove` 1s alternate, `text-blink` .4s, y el set Radix `slideUpAndFade`
  (`translateY(10px)` + fade) para popovers.
- Detalle distintivo: `lineAnimation` con **`steps(75, end)`** — animación escalonada
  (dithered/pixel-art feel) coherente con su estética de patterns pixelados.
- Easings: Tailwind default `cubic-bezier(.4,0,.2,1)` + `cubic-bezier(.16,1,.3,1)`
  (ease-out-expo-ish) y `(.34,1,.64,1)`.
- Los videos autoplay cargan el peso "wow"; el CSS anima casi nada on-scroll.
- **Gap notable: cero `prefers-reduced-motion` en su CSS.** (Nosotros lo tenemos como
  obligatorio — bien.)

### 2.5 Nav y footer

- Nav horizontal con dropdowns anidados (Product/Solutions), densidad alta.
- Footer **muy** denso: 5 grupos + columna entera de compliance (SOC2, HIPAA, ISO…) — el
  footer como argumento de venta enterprise.

---

## 3. OpenRouter (openrouter.ai)

### 3.1 Hero

- H1: "The Unified Interface For LLMs" — **`text-[56px] font-bold tracking-tight`**. Subhead
  corta ("Better prices, better uptime, no subscriptions."). CTAs "Get API Key" / "Explore
  Models".
- **El producto se presenta con números vivos**: fila de stats reales (100T tokens/mes,
  10M+ users, 70+ providers, 400+ models) + grid de logos de providers. El dato ES el
  marketing.
- **Fondo mesh 100% CSS** (sin imágenes):
  `radial-gradient(at 30% 20%, #281c40 0%, transparent 50%), radial-gradient(at 70% 80%, #0f1f2e 0%, transparent 50%), radial-gradient(#121221 0%, #0a0a10 100%)`
  — tres radiales (violeta arriba-izq, azul abajo-der, base) componen un mesh oscuro con
  variante light equivalente.
- **Starfield en CSS puro**: constelaciones hechas apilando radiales sub-pixel —
  `radial-gradient(circle at 18% 25%, #fff .3px, transparent .8px), radial-gradient(circle at 72% 18%, #fff .4px, ...)`
  ×N capas. Puntitos de 0.3–0.4px sin un solo asset.
- Fuentes: gordita / jakarta (sans redondeadas), **GeistMono** para código y números.

### 3.2 Ritmo de secciones

Nav (con search ⌘K) → hero + stats → provider grid → 4 feature blocks alternados (routing con
visualización de fallback, availability, price/performance con gráfico, data policies) →
Featured Agents (stat 250k+ apps) → grid de 3 apps con **datos reales de uso** → onboarding en
**3 pasos numerados** → blog (3 cards) → Featured Models con **tokens y trends semanales** →
footer 5 columnas. Historia: "todo el mercado de LLMs pasa por acá" contada con datos en vivo.

### 3.3 Glass / glow / gradiente

- **Spotlight hover que sigue el cursor**:
  `radial-gradient(circle at var(--px,50%) var(--py,50%), #ffffff59 0%, #e6e6e626 18%, transparent 40%)`
  — JS escribe `--px`/`--py` con la posición del mouse (mismo truco que el shine-beam de
  Linear, acá como highlight de fondo).
- Glow blanco suave central: `radial-gradient(circle at 50% 30%, #ffffff1a 0%, #ffffff0a 30%, transparent 70%)`.
- Glass moderado vía Tailwind: `backdrop-blur` de .5px/2px/8px/15px según superficie.
- 69 `mask-image` (edge fades de marquees y reveals), 45 radiales.

### 3.4 Animación

- Familia propia **`spawn-*`** (vocabulario de entrada consistente):
  - `spawn-stagger-in`: `.25s ease-out both`, `translateY(8px)` + fade, **stagger por
    `nth-child` con delays de 50ms**.
  - `spawn-fade-in`: `.4–.5s ease-out both` con delays escalonados `.1/.15/.2/.3/.4s`.
  - `spawn-fusion-slide-left/right`: `.35s cubic-bezier(.16,1,.3,1)` (ease-out-expo) —
    entradas laterales espejadas con 50ms de offset.
  - `spawn-shimmer`: sweep de `background-position` con highlight `#ffffff1a` en un
    `linear-gradient(110deg, transparent 25%, highlight 50%, transparent 75%)`.
  - `spawn-sparkle-a/b`: 2.5s infinite alternate (destellos decorativos).
- Más: `logo-scroll` (marquee), `pulse-green/red` .5s (indicadores de status vivo),
  accordions .2s. Un solo bloque `prefers-reduced-motion`.
- Todo CSS keyframes + clases utilitarias; sin gsap ni framer-motion detectables en la landing.

### 3.5 Nav y footer

Nav con **search prominente (⌘K)** como elemento central — coherente con un producto-catálogo.
Footer 5 columnas, ~25 links.

---

## Síntesis comparativa rápida

| | Linear | Neon | OpenRouter |
|---|---|---|---|
| Canvas | `#010102`/`#08090a` | `#0c0d0e` aprox | `#0a0a10` mesh |
| Hero H1 | ~80px/600/-0.022em | 72px/normal/tighter | 56px/bold/tight |
| Producto en hero | screenshots reales | carousel + videos | stats + logos |
| Profundidad | surface ladder + hairlines, **sin sombras** | gradient borders + luz de esquina | mesh + spotlight |
| Grain | tile CSS 256px blend overlay | noise.jpg/svg como asset | no |
| Animación | CSS + Motion quirúrgico, translateY(4px) | CSS puro, marquees + steps() | CSS puro, familia spawn-* |
| Easing firma | `cubic-bezier(.25,.46,.45,.94)` | `(.4,0,.2,1)` / `(.16,1,.3,1)` | `(.16,1,.3,1)` |
| Reduced motion | sí (12 bloques) | **no** | mínimo (1) |

---

## Patrones a robar para ArticleLens

Contexto: landing de una browser extension **local-first**, dark-only, Geist, hero = **demo
recreado en DOM del side panel**. Estos son los patrones que más rinden, en orden:

1. **Surface ladder + hairlines en lugar de sombras (Linear).** Canvas casi-negro con tinte
   (p.ej. `#0a0a0c`, nunca `#000`), 3–4 niveles de superficie separados por ~5% de luminancia,
   bordes `1px rgba(255,255,255,.08)` y highlight de 1px en el borde superior de paneles.
   Es exactamente el lenguaje para **recrear el side panel en DOM**: el mock del panel es una
   "surface 1" con hairline sobre el canvas, sin sombras que delaten "card de marketing".

2. **El demo como protagonista + mask de fade (Linear).** El panel recreado ocupa el ancho
   protagonista del hero y se funde con el fondo por abajo con
   `mask-image: linear-gradient(to bottom, #000 0% 60%, transparent 100%)`. Vende "esto es el
   producto de verdad", que es nuestra decisión de mapa (demo animado, no screenshot).

3. **Grain overlay estilo Linear (tile CSS, no asset gigante).** Un PNG/SVG de ruido de 256px
   en `mix-blend-mode: overlay`, `opacity .5–.9`, `pointer-events:none`, `border-radius:inherit`.
   Elimina el banding de nuestros gradientes y da textura premium sin JS ni imágenes pesadas
   (la variante de Neon — noise.jpg de página entera — es más cara; evitarla).

4. **Glass nav de Linear, con receta exacta.** Header fijo de 64px,
   `background: rgba(10,10,12,.8)`, `backdrop-filter: blur(20px)` (opcional `saturate(1.8)`),
   `border-bottom: 1px solid rgba(255,255,255,.08)`. Nuestra nav tiene 4 links — la densidad
   mínima hace que el glass luzca más.

5. **Headline two-tone de Neon.** H1/H2 en gris (`--ink-muted`) con los conceptos clave en
   `<strong>` blanco: "*Your articles, summarized* ***entirely on your device***". Jerarquía
   dentro del titular sin pesos extra — y Geist con `tracking-tight` clava la estética
   (bonus: Neon y OpenRouter ya usan Geist Mono; Geist es nativo de este lenguaje visual).

6. **Gradient border con glow localizado (Neon) para la card del demo y features.**
   `background: radial-gradient(35% 50% at 0 0, <acento>cc, transparent) border-box, linear-gradient(<gris-borde>, <gris-borde>) border-box`
   sobre borde transparente — o pseudo-elemento con `mask-composite: exclude` para anillos con
   gradiente. Un solo acento entrando por una esquina = "glow" sin parecer neón barato.
   Combinar con el fondo "luz de esquina" de Neon
   (`radial-gradient(100% 127% at 0 0, rgba(claro,.4), transparent 49%) + linear-gradient(165deg, oscuro₁, oscuro₂)`)
   para las feature cards.

7. **Mesh de hero 100% CSS (OpenRouter).** 2–3 `radial-gradient` de color de marca a baja alfa
   sobre base oscura (+ grain del punto 3 encima). Cero assets, cero JS, y es el fondo
   "gradientes/glow" que pide la estética objetivo. Opcional: starfield sub-pixel de radiales
   de .3px si queremos aire "tech".

8. **Sistema de animación mínimo y tokenizado (Linear + familia spawn de OpenRouter).**
   - Tokens: `--speed-quick: .1s`, `--speed-regular: .25s`,
     `--ease-out-quad: cubic-bezier(.25,.46,.45,.94)` (micro),
     `cubic-bezier(.16,1,.3,1)` (entradas).
   - Entradas on-scroll/on-load: fade + `translateY(4–8px)` — **4px como Linear, no 40** —
     .25–.5s, stagger de 50ms por hijo (patrón `spawn-stagger`).
   - Hover: `filter: brightness(1.2)` en .16s. Nada de scale/bounce.
   - `prefers-reduced-motion: reduce { animation: none }` global (Linear lo hace, Neon no —
     nosotros lo tenemos obligatorio en el mapa).
   - Todo esto es **CSS puro** — dato clave para el ticket 02: ninguna de las tres landings
     necesita gsap; Linear usa Motion solo quirúrgicamente. En Astro sin React alcanza con
     CSS + un IntersectionObserver chico (o scroll-driven animations con fallback).

9. **Qué NO animar (la lección más importante de las tres).** Headings estáticos, cero
   parallax, cero scroll-jacking, screenshots quietos. El movimiento se reserva para (a) el
   demo del hero — nuestro único "espectáculo", ya decidido — y (b) micro-feedback de hover.
   En Linear la entrada de secciones es casi subliminal (4px). La sutileza se logra por
   omisión, no por easing.

10. **Stats como social proof técnico (OpenRouter).** Una stat-row bajo el hero con números
    duros nuestros: **"0 requests con tu texto" / "100% en tu GPU" / "~2 GB de modelo local" /
    "3 providers opcionales"**. Para un producto privacy-first, los números son más creíbles
    que testimonials que no tenemos. En GeistMono, como OpenRouter.

11. **Marquee CSS con edge-masks (los tres lo usan).** Para la fila de "modelos/providers
    soportados" (Llama, Qwen, OpenAI, Anthropic, OpenRouter…): `translateX(calc(-100% - gap))`
    linear infinito + `mask-image` con fade de 80px en cada borde (receta exacta de Linear).
    Pausar con `:hover` y matar con reduced-motion.

12. **Un solo acento cromático, con disciplina de Linear.** Elegir UN color de marca (los
    "don'ts" de Linear: no usarlo de fondo, no sumar un segundo acento, radios 8px en CTAs —
    no pills) y dejar que el 95% de la página sea la escala de grises azulados. El glow y el
    gradient border del punto 6–7 son los únicos lugares donde el acento respira.

### Anti-patrones observados (evitar)

- Noise como JPG de página completa a q=100 (Neon): peso gratuito; usar tile CSS.
- Carousel en el hero (Neon): diluye el mensaje; nuestro demo único es más fuerte.
- Falta de `prefers-reduced-motion` (Neon): inaceptable para nosotros (regla de mapa).
- Repetir 5 veces el mismo layout de feature block (Linear) funciona a su escala de contenido,
  pero con nuestras 4–5 historias conviene la alternancia de Neon (split / grid / stats).
