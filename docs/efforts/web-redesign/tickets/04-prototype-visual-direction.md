---
title: 'Dirección visual (prototipos)'
label: wayfinder:prototype
status: closed
assignee: victorbejas (session 2026-07-17)
closed: 2026-07-17
blocked-by: [01-research-references.md]
map: ../map.md
---

## Question

¿Cuál es la dirección visual de la identidad nueva? Decidido: Geist, dark-only, gradientes +
glow + glass, animación sutil. Abierto: **cómo** se combinan — y eso se decide reaccionando a
prototipos, no discutiendo en abstracto.

Producir **2–3 direcciones en código** (hero + una sección representativa cada una, con los
patrones extraídos del research de referencias) variando:

- Paleta: ¿acento de color (cuál) o monocromo + glow blanco? ¿gradientes de qué familia?
- Temperatura del glass: ¿cards con backdrop-blur prominente o sutil? ¿borders con gradiente?
- Densidad tipográfica: ¿hero gigante estilo Linear o más contenido y compacto?
- Fondo: ¿radial glows, grain/noise, grid pattern, o limpio?

Consultar `/emil-design-eng` al construirlas. El usuario reacciona (HITL), se elige/mergea una
dirección, y la resolución fija los **tokens** de la identidad (paleta, radios, sombras/glow,
escala tipográfica) para la spec.

Bloqueado por: [Research: deconstruir las referencias](01-research-references.md).

## Resolution (2026-07-17)

Prototipo con 3 direcciones (hero + privacy stat-row + cards de modelos cada una, Geist real
embebida): https://claude.ai/code/artifact/c6ec4da6-a612-4f7e-bd35-9f2b968a7af6
(A Precisión = mono Linear · B Óptica = acento + gradient borders · C Atmósfera = mesh violeta).

**Elegida: B "Óptica" con el azul de la extensión** (el usuario pidió reemplazar el cian por el
`--primary` del side panel; iterado y confirmado). **Tokens fijados para la spec:**

- **Paleta**: canvas `#0b0d0e`; surfaces `#121415` / `#161819` / `#1b1d1f`; hairlines
  `rgba(255,255,255,.09)` (strong `.15`); ink `#f5f7f8`, muted `#9ba1a6`, faint `#6b7075`.
- **Acento = `#6ea8fe`** (mismo `--primary` de la extensión; foreground `#0b1220` — el par ya
  shipping en el panel). Deep `#2f6fe4`. CTA primario: gradiente `180deg #8fc0ff → #5c9bfd`,
  radio 8px, texto `#0b1220`.
- **Tipografía**: Geist única familia. H1 clamp 40–72px, tracking −0.032em, lh 1.04;
  H2 28–40px, tracking −0.025em. **Headlines two-tone**: base gris muted w500 + `<strong>`
  blanco w600 (técnica Neon). Body 17px/1.6 muted. Eyebrow 12px uppercase +0.08em en acento.
  Métricas/números en `ui-monospace`, `tabular-nums`.
- **Profundidad**: sin drop-shadows — hairlines + top-edge highlight
  (`inset 0 1px 0 rgba(255,255,255,.06)`). **Gradient borders** (borde transparente + doble
  background `border-box`) con glow azul entrando por la esquina sup-izq
  (`radial rgba(110,168,254,.75–.8) → gris borde`) en panel del hero y card destacada;
  "luz de esquina" (`radial 100% 127% at 0 0`) en cards. Radios: 8 botones / 12 cards / 14 panel.
- **Fondo**: 2 radiales azules de baja alfa (`rgba(110,168,254,.13)` + `rgba(47,111,228,.10)`)
  + **grain** tile SVG 256px `mix-blend-mode: overlay` opacity .55. Panel del hero con
  `mask-image` fade inferior (62% → transparent).
- **Nav glass**: 64px, `blur(20px) saturate(1.6)`, canvas al 78%, border-bottom hairline.
- **Motion**: entradas fade + translateY(5px), .5s `cubic-bezier(.16,1,.3,1)`, stagger ~70ms;
  hover `brightness(1.12–1.15)` .16s; active `scale(.97)`; reduced-motion mata todo.
