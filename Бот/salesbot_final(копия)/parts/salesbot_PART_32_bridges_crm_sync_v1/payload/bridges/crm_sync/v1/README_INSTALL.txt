
crm_sync/v1 — связка CRM ↔ модули
---------------------------------
Назначение:
  - Синхронизация статусов сделок (deal.status)
  - Таймлайн событий (add_note)
  - Профили менеджеров (ensure_manager_profile)
  - Массовая синхронизация (bulk_sync_deals)
  - Маппинг статусов из внутренних модулей

Зависимости:
  - bridges.crm_api_bridge.v4 (CRMClient, Deal, Note)
  - core/state/v1 (kv как локальный кеш)

Эндпоинты:
  POST /crm_sync/v1/status/{deal_id}     body: {status, reason?}
  POST /crm_sync/v1/timeline/{deal_id}   body: {event, payload?}
  POST /crm_sync/v1/manager/ensure       body: {id, name?, phone?, email?}
  POST /crm_sync/v1/bulk_sync            body: {deals:[{id,status,title?,amount?,currency?}]}
  GET  /crm_sync/v1/health
