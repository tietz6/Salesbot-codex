
mini_webkit/v3 — lightweight UI-layer for previews (Telegram-friendly)
---------------------------------------------------------------------
Что это:
  - Лёгкий рендер HTML без внешних шаблонизаторов
  - Просмотр бандлов, диалогов, итогов экзамена
  - Мобильный адаптив (inline CSS), быстрый open-in-Telegram WebView

Эндпоинты:
  GET  /mini/v3/health
  POST /mini/v3/preview/bundle      (body: json bundle/pricing)
  POST /mini/v3/preview/dialog      (body: {history:[{role,content},...]})
  POST /mini/v3/preview/exam        (body: exam report)
  GET  /mini/v3/version

Установка:
  REPLACE → apps/mini_webkit/v3
  post_hooks: rebuild_routes + touch_startup
