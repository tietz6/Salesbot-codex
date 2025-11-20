
public_miniapp/v1 — public miniapp endpoints (Telegram-ready)
-------------------------------------------------------------
Функции:
  - генерация публичных shortlinks
  - simple auth-lite для мини-приложения
  - открытие preview страниц mini_webkit/v3 в WebView Telegram
  - поддержка параметров t.me?startapp=<payload>

Роуты:
  GET  /miniapp/v1/health
  GET  /miniapp/v1/open/bundle/{key}
  GET  /miniapp/v1/open/dialog/{key}
  GET  /miniapp/v1/open/exam/{key}
  POST /miniapp/v1/create_key  (body → json сохраняется в kv)

Сохранение данных:
  - KV storage через core/state/v1
  keys формата: miniapp:<random>
