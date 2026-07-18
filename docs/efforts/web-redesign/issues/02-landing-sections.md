# 02 — Secciones de la landing (estáticas, EN/ES)

**What to build:** la landing multi-sección completa en su forma **estática** (sin animación
todavía), en ambos idiomas. Tras este ticket, `/` y `/es/` muestran, en orden: hero (eyebrow,
H1 two-tone, sub, CTA primario + GitHub, y un **placeholder estático del panel** donde luego irá
el demo animado) → privacidad (claim + stat-row de 4 números) → cómo funciona (4 pasos
numerados) → elige tu modelo (3 cards: On-device destacada · Free cloud OpenRouter · Tu key
OpenAI/Anthropic) → banda compacta open source → sección CTA de cierre. Todo el copy vive en los
diccionarios EN/ES; los anchors de la nav apuntan a las secciones reales.

**Blocked by:** 01 — Identidad "Óptica" + shell i18n.

**Status:** ready-for-agent

- [ ] Las 6 secciones del cuerpo maquetadas con el layout propio de cada una (headlines two-tone, gradient borders con glow donde corresponde, luz de esquina en cards, grain overlay), fieles a la dirección B del prototipo.
- [ ] Copy de todas las secciones en los diccionarios EN + ES (mismas keys); nada hardcodeado.
- [ ] Stat-row de privacidad con los 4 números ("0 requests con tu texto", "100% en tu GPU", "1 descarga ~2 GB", "3 providers opcionales") en mono/tabular-nums.
- [ ] "Elige tu modelo": 3 cards con la card On-device destacada (glow azul de esquina); refleja los 3 caminos del chooser de la extensión.
- [ ] CTAs solo en hero, nav y sección de cierre — nada inline entre secciones.
- [ ] Anchors de la nav (Privacidad / Cómo funciona / Modelos) scrollean a la sección correcta.
- [ ] Responsive: ≤760 px stat-row a 2 columnas, cards a 1 columna, sin scroll horizontal.
- [ ] `pnpm build:web` y `pnpm lint:web` pasan en ambos locales.
