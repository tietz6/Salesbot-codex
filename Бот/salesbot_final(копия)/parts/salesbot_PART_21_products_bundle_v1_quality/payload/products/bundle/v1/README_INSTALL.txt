
products/bundle/v1 — QUALITY UPGRADE
------------------------------------
Улучшения:
  - Валюта: KGS (дефолт), USD, UZS
  - Курс валют из ENV: KGS_USD, KGS_UZS (или дефолтные)
  - Скидки: coupon %-скидка, promo фиксированная скидка
  - НДС/VAT: VAT_RATE (например, 0.12)
  - Вспомогательные функции: deal_title()
  - build_custom(): сборка произвольного набора элементов
  - apply_pricing(): финальное ценообразование с налогами/скидками

Пример:
  bundle = build_bundle(song=True, video=True, premium=False)
  priced = apply_pricing(bundle, currency="USD", coupon=10, vat=True)
  title = deal_title(bundle)
