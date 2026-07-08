# v9 — OpenRouter como tercer cloud provider (modelos free)

## Context

Hoy el escape hatch cloud (v6) soporta OpenAI + Anthropic vía Vercel AI SDK, ambos pagos con key
propia. OpenRouter agrega un tercer adaptador con una diferencia de producto: **modelos gratuitos**
(`:free`) — el usuario crea una key gratis en openrouter.ai/keys y resume sin pagar por token.
La arquitectura existente ya tiene las costuras exactas para esto (union `CloudProvider`, factory
`resolveModel`, key storage genérico `apiKey:${provider}`, lazy cloud chunk) — el plan extiende esas
costuras sin reestructurar nada.

**Hechos investigados (docs OpenRouter, julio 2026):**

- Provider oficial AI SDK: **`@openrouter/ai-sdk-provider@^3.0.0`** — compatible con AI SDK v7
  (tenemos `ai ^7.0.6`). ESM-only (Vite lo bundlea; el requisito Node 22 es solo build-time).
  `createOpenRouter({ apiKey, headers? })` → `openrouter(modelId)` → mismo `streamText` de siempre.
  Elegido sobre reusar `createOpenAI({ baseURL })` porque `@ai-sdk/openai` tiende al Responses API
  (OpenRouter solo soporta chat completions) y mete params OpenAI-specific.
- Base URL `https://openrouter.ai/api/v1`, Bearer auth. **CORS habilitado para llamadas directas
  desde browser** — a diferencia de Anthropic, no hace falta header especial. Headers opcionales de
  atribución: `HTTP-Referer` + `X-OpenRouter-Title`.
- Free tier: sufijo `:free`, precio $0, rate limits ~**20 req/min y 50/día** (1000/día con $10 de
  créditos comprados), **sin garantía de uptime** (429/502/503 son normales — hay que mapearlos).
- Modelos free fuertes para resumir (instruction-following + multilingüe; los de código quedan
  afuera): `google/gemma-4-31b-it:free` (multilingüe 140+ idiomas — ideal para posts es/en),
  `openai/gpt-oss-120b:free` (más fuerte), `openai/gpt-oss-20b:free` (baja latencia).

**Decisiones del usuario:** 3 modelos curados. Selector: On-device primero, después grupos Cloud —
providers por API key (OpenAI, Anthropic) y un grupo aparte de **modelos gratuitos OpenRouter**,
destacando que OpenRouter **también requiere API key** (gratuita).

## Sin cambios (por diseño)

Protocolo de mensajes (`messages.ts`), mecánica de keys (`useProviderSettings.ts` es genérico —
`apiKey:openrouter` sale gratis), estructura lazy (el provider nuevo se importa solo desde
`cloud.ts` → cae en el chunk lazy existente), `inference-backend.ts`, `cloud-estimate.ts` (con
precios $0 estima $0 correctamente), `useSummarize`/`useCloudBackend`/`state.ts`.

## Pasos

### 0. Dependencia

```bash
pnpm add @openrouter/ai-sdk-provider@^3.0.0
```

### 1. `src/shared/models.ts` — tipos + registry

- `CloudProvider = 'openai' | 'anthropic' | 'openrouter'` + entrada en `CLOUD_PROVIDER_LABEL`
  (`openrouter: 'OpenRouter'`). TS fuerza actualizar todo `Record<CloudProvider, …>` (KEY_HELP) —
  la costura de mantenibilidad trabajando.
- Helper nuevo:
  ```ts
  /** True cuando ambos precios de lista son $0 (variantes `:free` de OpenRouter). */
  export function isFreeModel(spec: CloudModelSpec): boolean {
    return spec.inputCostPer1M === 0 && spec.outputCostPer1M === 0
  }
  ```
- 3 entradas nuevas en `CLOUD_MODELS` (**verificar IDs/context en openrouter.ai/models al
  implementar — los free rotan**; comentario en el registry debe decirlo):
  - `google/gemma-4-31b-it:free` — «Gemma 4 · 31B (free)», ~128K ctx, costos 0/0,
    `recommended: true`, note: multilingüe, pick recomendado de OpenRouter, free tier rate-limited.
  - `openai/gpt-oss-120b:free` — «GPT-OSS · 120B (free)», 131_072 ctx, 0/0, note: más fuerte,
    más lento/menos disponible.
  - `openai/gpt-oss-20b:free` — «GPT-OSS · 20B (free)», 131_072 ctx, 0/0, note: rápido, fallback.
- Actualizar doc comment del archivo (OpenAI / Anthropic / OpenRouter).

### 2. `src/inference/cloud.ts` — adaptador + errores

- `resolveModel`: branch nuevo antes del fallthrough OpenAI:

  ```ts
  import { createOpenRouter } from '@openrouter/ai-sdk-provider'

  if (spec.provider === 'openrouter') {
    // OpenRouter soporta CORS browser-directo — no necesita header de opt-in como Anthropic.
    return createOpenRouter({ apiKey })(spec.id)
  }
  ```

  (Headers de atribución `HTTP-Referer`/`X-OpenRouter-Title` opcionales — omitir salvo que se
  quiera figurar en el leaderboard; fuerzan preflight extra.)

- `toUserMessage`:
  - `providerName` pasa de ternario hardcodeado a `CLOUD_PROVIDER_LABEL[spec.provider]`
    (import valor desde models.ts — hoy es type-only).
  - **429**: si `spec.provider === 'openrouter' && isFreeModel(spec)` → mensaje específico del
    free tier (~20 req/min, 50/día sin créditos; esperá y reintentá o elegí otro modelo). El
    genérico queda para los pagos.
  - **502/503 branch nuevo**: OpenRouter los devuelve cuando el upstream del modelo free no tiene
    capacidad → «modelo temporalmente no disponible upstream; reintentá o elegí otro modelo».
  - Los strings de error quedan en inglés hardcodeado como los actuales (i18n de errores
    cross-context está deferred — no migrar a medias).
- Actualizar doc comment del archivo.
- `CloudBackend.summarize` no cambia: mismo `streamText`/`textStream`; si OpenRouter no reporta
  `usage`, el fallback `estimateTokens` existente cubre; costo $0 sale de `estimateCost`.

### 3. `wxt.config.ts` — CSP

Agregar `https://openrouter.ai` a `connect-src` (el API vive en `/api/v1`, mismo origin) +
actualizar comentario.

### 4. UI

**`ModelSelector.tsx`** — estructura acordada con el usuario:

- Grupo On-device igual que hoy.
- Grupos cloud derivados del registry (registry order = source of truth), no hardcodeados:
  `Cloud · OpenAI`, `Cloud · Anthropic`, y para openrouter un label distintivo tipo
  `OpenRouter · Modelos gratis (requiere API key)` — deja claro upfront que free ≠ sin key.
- Filas free: donde hoy renderiza `$in/$out per 1M`, si `isFreeModel(spec)` mostrar `Free`/`Gratis`
  (i18n), nunca «$0/$0 per 1M».

**`ModelCard.tsx`**:

- Badge de precio → `Free` para modelos free.
- Línea extra (i18n `card.freeNote`) para free: «nivel gratuito — solicitudes diarias limitadas;
  puede no estar disponible temporalmente». Los 429/503 son la UX definitoria de `:free` — avisar.

**`CloudKeyPanel.tsx`**:

- `KEY_HELP.openrouter: 'openrouter.ai/keys'` (compile falla hasta agregarlo — bien).
- El guide `<details>` OpenAI-only queda gateado como está; OpenRouter no necesita guide
  (las keys funcionan al toque, sin allowlist por modelo).
- El flujo `needs-key` existente ya bloquea el run sin key de OpenRouter — nada que cambiar.

**Badges de costo ($0 → «Free»)**:

- Pre-run (`StatusView.tsx`): `estCostUsd === 0` → ` · Free` en vez de `~$0`.
- Post-run (`SummaryResult.tsx`, badge Wallet): `costUsd === 0` → `Free`.
- `format.ts` (`formatCost`) queda intacto — «Free» es decisión de producto en la vista, no del
  formatter.

### 5. i18n — `locales/en.yml` + `es.yml`

Keys nuevas: `selector.free` (Free/Gratis), label del grupo OpenRouter
(p.ej. `selector.openrouterGroup`: «OpenRouter · Free models (requires API key)» /
«OpenRouter · Modelos gratis (requiere API key)»), labels de grupo por provider si el actual
`selector.cloudGroup` se reemplaza, `card.free`, `card.freeNote`, `cost.free`.

### 6. Doc comments desactualizados

Grep de listas de providers viejas: headers de `useCloudBackend.ts`, `useProviderSettings.ts`
(ejemplo `apiKey:openai`/`apiKey:anthropic`), `models.ts`, comentario CSP en `wxt.config.ts`.

### 7. Post-implementación (workflow del repo)

- Guardar este plan en `docs/plans/v9-openrouter-free-models.md`.
- Actualizar `docs/context/app-context.md` (stack, invariantes: CORS OpenRouter sin header,
  free tier limits; iteration history v9; current state).

## Riesgos

1. **Drift de IDs de modelos free (el mayor)**: los `:free` rotan/se deslistean. Verificar los 3
   IDs en openrouter.ai/models al implementar; un ID muerto cae en el mensaje 404 (que ahora nombra
   OpenRouter correctamente).
2. **Compat provider v3 ↔ AI SDK v7**: declarado compatible; un mismatch de spec de modelo es
   error de compile → se detecta en `pnpm compile`.
3. **`usage` ausente en algunos upstreams free** → fallback `estimateTokens` existente cubre.
4. **Flakiness del free tier** (429/502/503) → cubierto por los branches nuevos; QA debe provocar
   el 429 a propósito.

## Verificación

Build-time:

1. `pnpm compile` (esperá que falle primero si falta `KEY_HELP.openrouter` — prueba de la costura).
2. `pnpm lint` + `pnpm format:check` + `pnpm build`.
3. En `.output/chrome-mv3`: CSP del manifest incluye `https://openrouter.ai`; grep de
   `openrouter.ai/api` en chunks → solo en el chunk lazy `cloud-*.js`, no en el panel eager.

Browser QA (load unpacked): 4. Selector: On-device / Cloud·OpenAI / Cloud·Anthropic / OpenRouter·gratis; filas free muestran
«Free», no «$0/$0». 5. Modelo free sin key → `needs-key`; hint `openrouter.ai/keys`; guardar key → Ready; persiste;
Delete funciona. 6. Resumir artículo real con Gemma free: badge pre-run `~N tokens · Free`; streaming tipea; badge
Wallet post-run «Free»; tokens poblados. 7. Errores: key basura → mensaje 401 nombra OpenRouter; ID inválido temporal → 404 nombra
OpenRouter; martillar >20 req/min → mensaje 429 de free tier. 8. Regresión: un run OpenAI + un run Anthropic (el refactor de labels tocó sus paths de error) +
un run local WebGPU. 9. Network tab: requests a `https://openrouter.ai/api/v1/...`, cero violaciones CSP en consola. 10. Chrome en español → strings nuevos en español.

## Archivos críticos

- `src/shared/models.ts` — union, label map, `isFreeModel`, 3 entradas registry
- `src/inference/cloud.ts` — `resolveModel` branch, `toUserMessage` refactor + 429/503
- `wxt.config.ts` — CSP
- `src/features/summarize/ui/ModelSelector.tsx` — grupos por provider + «Free»
- `src/features/summarize/ui/ModelCard.tsx` — badge Free + freeNote
- `src/features/summarize/ui/CloudKeyPanel.tsx` — KEY_HELP
- `src/features/summarize/ui/StatusView.tsx` + `SummaryResult.tsx` — badges $0 → Free
- `locales/en.yml` + `locales/es.yml`
- `docs/plans/v9-openrouter-free-models.md` + `docs/context/app-context.md` (post)
