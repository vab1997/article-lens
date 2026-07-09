# Rename: Local Resumer → ArticleLens

## Context

The app started as local-only inference ("Local Resumer"), but since v6 (OpenAI/Anthropic) and
v9 (OpenRouter free models) it is **local-first + optional cloud** — the name and README no longer
match reality. README still claims "No servers, no API keys, your content never leaves the machine"
(false since v6) and mentions zero cloud features. New name decided in grilling: **ArticleLens**,
with the description: *"AI-powered browser extension that turns any article into a clean,
structured summary. Run models locally for privacy or use your favorite cloud provider."*

## Decisions from grilling

- **Name: ArticleLens** (decided). Conflict check done via web search: no existing "ArticleLens"
  extension on the Chrome Web Store; adjacent names exist (Google Lens family, MyLens AI web tool)
  but no collision. Extension is unpublished but will be published soon — name validated now.
- **Scope: everything + GitHub repo rename.** Manifest/locales, panel title, error strings,
  package.json, README (full rewrite), app-context, CLAUDE.md goal line, and
  `gh repo rename` on GitHub. **Local folder `~/projects/local-resumer` stays** (user renames
  manually later if desired — avoids breaking Claude memory path / configs).
- **README: full rewrite** repositioning as local-first + optional cloud; fix all stale claims.
- **Constraint found:** Chrome manifest `description` max **132 chars**; the full description
  (~155) goes to README / future store listing, a shortened version goes in the manifest.

## Naming conventions

| Where | Value |
|---|---|
| Display name (manifest, UI, docs) | `ArticleLens` |
| Slug (package.json name, GitHub repo) | `article-lens` |
| Manifest description EN (≤132 chars) | `Turn any article into a clean, structured summary. Run AI models locally for privacy or use your favorite cloud provider.` (123) |
| Manifest description ES (≤132 chars) | `Convierte cualquier artículo en un resumen claro y estructurado. IA local para privacidad o tu proveedor cloud favorito.` (~121) |
| Full description (README intro, store listing) | User's version verbatim |

## Changes

### 1. Locales — `locales/en.yml`, `locales/es.yml`
- `extName: ArticleLens`, `extDescription:` (short versions above), `actionTitle: Open ArticleLens`
  / `Abrir ArticleLens`, and the `webgpu.intro` line ("Local Resumer runs the model…" →
  "ArticleLens runs the model…" / ES equivalent).

### 2. Code strings
- `entrypoints/sidepanel/index.html:6` — `<title>ArticleLens</title>`.
- `src/inference/backend.ts:20,29` — two WebGPU error messages mention "Local Resumer" → "ArticleLens".

### 3. `package.json`
- `name: "article-lens"`, `description:` updated to reflect local + cloud (this also renames the
  `pnpm zip` artifact, which WXT derives from the package name).

### 4. `README.md` — full rewrite (keep structure, fix positioning)
Source of truth for positioning: `docs/context/app-context.md` "What it is" (already accurate).
- **Title + intro**: ArticleLens + user's full description; local-first framing with cloud
  escape hatch. Kill the "No servers, no API keys" absolute claim — scope it to local mode.
- **Features**: "100% local inference" → "Local inference by default"; add **Cloud providers**
  bullet (OpenAI / Anthropic / OpenRouter with your own API key, OpenRouter `:free` models = $0,
  explicit "cloud sends the article to the provider" privacy note); add model selector +
  hardware feasibility (v5) — currently missing.
- **How it works / Model**: note cloud runs are single-pass on the panel thread via Vercel AI SDK
  (lazy-loaded), local runs use the worker; keep the rest.
- **Roadmap**: remove "Model selection" (shipped in v5); keep WASM fallback, KV/prefix-cache,
  Firefox polish.
- **Docs section**: `docs/plans/v1..v4` → `v1..v9`.
- Dev/build/structure sections stay as-is (still accurate).

### 5. `docs/context/app-context.md`
- Line 1: `# ArticleLens — App Context`. Grep for any other "Local Resumer" mentions and update.

### 6. `CLAUDE.md`
- Goal line says "runs an AI model **locally in the browser** (no server inference)" — stale;
  update to local-first + optional cloud, and name the app ArticleLens.

### 7. GitHub repo rename
- `gh repo rename article-lens` (gh updates the local `origin` remote automatically; GitHub
  redirects old URLs). Run after code changes are committed.

### Untouched (deliberately)
- `docs/plans/v*.md` including `v1-local-resumer-plan.md` filename — historical record.
- Local directory name `~/projects/local-resumer`.
- Note: `src/inference/prompt.ts` has uncommitted changes unrelated to this task — leave alone.

## Verification

1. `wc -c` check both locale `extDescription` strings ≤132.
2. `pnpm compile && pnpm lint && pnpm build` — clean.
3. Load `.output/chrome-mv3/` unpacked: `chrome://extensions` shows **ArticleLens** + new
   description; toolbar tooltip "Open ArticleLens"; panel tab title "ArticleLens"; switch browser
   to ES and confirm ES strings.
4. `git remote -v` shows `article-lens` after repo rename; old GitHub URL redirects.
5. Update `docs/context/app-context.md` per project workflow (done as part of change set).
