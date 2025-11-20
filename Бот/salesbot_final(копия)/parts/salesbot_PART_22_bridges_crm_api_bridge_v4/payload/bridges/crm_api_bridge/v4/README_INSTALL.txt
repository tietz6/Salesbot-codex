
crm_api_bridge/v4 — Quality Upgrade
-----------------------------------
Улучшения:
  - Явные ошибки CRMError с кодами (bad_request, unauthorized, timeout, server_error, parse_error)
  - Жёсткие таймауты и ретраи через integrations/patch_v3.http_client
  - Нормализация ответов: ожидаем JSON, достаём полезные поля
  - Валидаторы входных данных (минимальная проверка)
  - Методы idempotent by design: upsert_contact, create_deal, add_note
  - Health-роут для дымового теста

ENV (пример):
  CRM_API_BASE=https://your-crm/api
  CRM_API_TOKEN=***
  CRM_API_TIMEOUT=20
  HTTP_TIMEOUT=15
  HTTP_RETRIES=3
