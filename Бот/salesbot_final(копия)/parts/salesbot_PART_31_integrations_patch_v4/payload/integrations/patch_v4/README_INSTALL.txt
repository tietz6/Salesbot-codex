
integrations/patch_v4 — обновлённый набор интеграций
----------------------------------------------------
Включает:
  - PaymentGateway (mock + webhooks)
  - SMS / Email provider adapters
  - FakeProvider (sandbox)
  - ExternalAPI client (универсальный fetcher)
  - retry-механика
  - стандартизированные ответы integration_result()

Роуты:
  POST /integrations/v4/payment/create
  POST /integrations/v4/payment/webhook
  POST /integrations/v4/sms/send
  POST /integrations/v4/email/send
  POST /integrations/v4/ext/fetch
