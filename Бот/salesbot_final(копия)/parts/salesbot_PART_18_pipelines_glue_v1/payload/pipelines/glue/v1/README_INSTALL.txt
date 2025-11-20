
Pipelines Glue v1
Назначение:
  - Связка: ProductBundle -> CRM Deal -> Invoice (Payments)
  - Единый оркестратор: создание контакта, сделки и инвойса
  - Роуты FastAPI для быстрого тестирования

Маршруты:
  POST /glue/build_bundle {song?, video?, premium?}
  POST /glue/create_deal {title, amount, currency, contact:{...}}
  POST /glue/buy_bundle {song?, video?, premium?, contact:{...}}
  GET  /glue/invoice_status/{invoice_id}
