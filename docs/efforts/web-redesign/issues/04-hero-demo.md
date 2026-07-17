# 04 — Demo animado del side panel en el hero

**What to build:** reemplazar el placeholder del hero por el demo animado recreado: una ventana
browser mock (dots + URL) con el artículo a la izquierda y el panel idealizado a la derecha,
que corre la coreografía completa (~9 s) en loop — auto-click "Summarize" → progreso en dos
fases → streaming de título y TL;DR por palabra con caret → 3 puntos con stagger → métricas →
hold → fade y vuelve a empezar. Trigger on-load; hover sobre el stage pausa; en mobile la
columna del artículo se oculta (panel solo); con `prefers-reduced-motion` se muestra el estado
final estático. La coreografía exacta (tiempos, textos) vive en la resolución del ticket 05 del
mapa (prototipo aprobado).

**Blocked by:** 03 — Sistema de animación.

**Status:** ready-for-agent

- [ ] Ventana browser mock con gradient border azul de esquina + mask de fade inferior; split artículo/panel.
- [ ] Coreografía completa implementada con Motion (`animate` sequences) + driver de typing propio, en loop, siguiendo tiempos del prototipo.
- [ ] Hover sobre el stage pausa el loop; al salir continúa.
- [ ] Trigger on-load (o on-view); `prefers-reduced-motion` muestra el estado final estático sin loop.
- [ ] Mobile (≤760 px): la columna del artículo se oculta, queda el panel solo; sin scroll horizontal.
- [ ] Textos del demo en el diccionario (o marcados como contenido de demo, no traducibles si así se decide) — coherente en ambos locales.
- [ ] `pnpm build:web` y `pnpm lint:web` pasan; JS total dentro del presupuesto.
