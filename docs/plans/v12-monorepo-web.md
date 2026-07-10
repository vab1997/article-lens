# v12 — Monorepo pnpm + web page (Astro) con privacy policy

## Context

La publicación en el Web Store quedó bloqueada solo por la URL de privacy policy. Decisión:
producto tendrá web page propia (hostea privacy + landing). Se reorganiza el repo como monorepo
pnpm con la extensión y la web. La web replica el estilo de `~/projects/skillstui.sh`
(https://skillstui.sh — web previa del usuario): dark, minimal, terminal-style, simple por ahora.

## Decisiones (grilled 2026-07-09)

- **Estructura: `apps/extension` + `apps/web`**, `pnpm-workspace.yaml` en root.
- **Deploy: Vercel con dominio `*.vercel.app`** por ahora (privacy URL provisoria; dominio propio
  después con redirect).
- **Hero visual: screenshot estático** (placeholder enmarcado hasta que el usuario capture la
  real — la misma del store).
- **Privacy: EN + ES** (`/privacy` y `/es/privacy`).

## Verificado en exploración

- Move seguro: `scripts/copy-ort.mjs` resuelve por `__dirname`, `make-icons.py` por `__file__`,
  `tsconfig.json` relativo, no hay CI workflows. Nada asume el path absoluto del repo.
- Referencia skillstui.sh: Astro 6 + Tailwind v4 (`@tailwindcss/vite`) + Geist variable +
  `@lucide/astro` + adapter Vercel con web analytics; Prettier con los mismos plugins que ya usa
  la extensión. Página única de ~120 líneas: logo, comando con copy-button (vanilla JS), botones
  GitHub/secondary, "How it works" numerado `[1]..[4]`, footer.

## Cambios

### 1. Reorganización monorepo
- `git mv` a `apps/extension/`: `entrypoints/`, `src/`, `locales/`, `public/`, `scripts/`,
  `assets/`, `wxt.config.ts`, `tsconfig.json`, `eslint.config.*`, `.prettierrc*`, `package.json`
  (nombre queda `article-lens`).
- Quedan en root: `docs/`, `.claude/`, `CLAUDE.md`/`AGENT.md`, `README.md`, `.gitignore`.
- Root nuevo: `pnpm-workspace.yaml` (`apps/*`) + `package.json` root privado con scripts proxy
  (`dev:ext`, `build:ext`, `dev:web`, `build:web` vía `pnpm -F`).
- Lockfile único de workspace (regenerar con `pnpm install`).
- `CLAUDE.md`/`AGENT.md` + `README.md`: mapa monorepo + comandos nuevos.

### 2. apps/web — scaffolding Astro (espejo de skillstui.sh, sin React)
- Deps: `astro`, `@astrojs/vercel`, `@vercel/analytics`, `tailwindcss` + `@tailwindcss/vite`,
  `@fontsource-variable/geist`, `@lucide/astro`, prettier (+ plugins astro/tailwind/organize),
  `eslint-plugin-astro`. **Sin React** — el hero es imagen estática y el copy-button de la
  referencia ya es vanilla JS.
- `astro.config.mjs`: tailwind vite plugin + adapter vercel (webAnalytics).
- `src/layouts/Layout.astro`: adaptación del de skillstui (SEO/OG/twitter/JSON-LD), `SITE`
  constante = `https://article-lens.vercel.app`, dark por defecto.
- `src/pages/index.astro`: columna izquierda — icono (128px del squircle) + "ArticleLens",
  descripción (la larga aprobada), CTA: botón Chrome Web Store en estado "Coming soon"
  (deshabilitado hasta publicar) + botón GitHub; "How it works" `[1]..[4]` (abrir panel → elegir
  local o cloud → Summarize con prompt de permiso → export .md). Columna derecha — screenshot
  en frame estilizado (`public/screenshot.png`; placeholder CSS mientras no exista).
- `src/pages/privacy.astro` + `src/pages/es/privacy.astro`: política basada en
  `docs/store/dashboard.md` (data-use real: local por defecto, cloud opt-in al proveedor
  elegido, keys en storage local, cero telemetría/servidores propios, contacto). Fecha de
  vigencia + link cruzado EN↔ES.
- `src/components/footer.astro`: © año, GitHub, link privacy, switch idioma.
- `public/`: favicon (reusar `icon/32.png` + un favicon.svg del mark), `icon-128.png`.

### 3. Integración con el submit
- `docs/store/dashboard.md`: privacy URL → `https://article-lens.vercel.app/privacy`
  (nota: confirmar el nombre real del proyecto Vercel al deployar).
- Listing EN/ES: agregar link a la web al final.

## Tareas del usuario (post-implementación)

- Conectar el repo a Vercel: proyecto nuevo, **root directory = `apps/web`** (framework Astro
  auto-detectado). Confirmar URL final.
- Capturar `apps/web/public/screenshot.png` (misma captura 1280×800 del store).

## Verification

1. `pnpm install` en root resuelve el workspace; `pnpm -F article-lens compile && build` —
   manifest idéntico al de v11 (diff contra el actual).
2. `pnpm -F web build && pnpm -F web preview` → curl `/`, `/privacy`, `/es/privacy` responden;
   revisar HTML (title/OG/canonical).
3. `python3 apps/extension/scripts/make-icons.py` sigue funcionando post-move (venv scratchpad).
4. Extensión: cargar `.output/chrome-mv3` unpacked y correr un resumen (smoke — usuario).

## Entrega (pedido explícito del usuario)

- **SIN commits**: todo queda en `git add` (staged) para review manual del usuario.
- Al terminar: correr **/code-review** sobre los cambios implementados y reportar findings.
