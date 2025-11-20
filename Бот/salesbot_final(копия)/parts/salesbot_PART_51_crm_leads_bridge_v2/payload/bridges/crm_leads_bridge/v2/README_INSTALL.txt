
crm_leads_bridge/v2 — мост Тренер ⇄ CRM
---------------------------------------
Назначение:
  • Подтянуть лиды из CRM (mock/adapter), отдать менеджеру тренеру
  • Сопоставить профиль менеджера (из dialog_memory) с результатами по лидам
  • Скорить «выравнивание» речи/стиля и рекомендовать тренировки
  • Принять вебхуки CRM и обновить внутренние статусы
  • Простые фильтры: статус, дедлайн, бюджет, цель подарка

Основные роуты:
  GET  /crm_bridge/v2/health
  GET  /crm_bridge/v2/config
  POST /crm_bridge/v2/pull_leads         {filters?}
  POST /crm_bridge/v2/push_result        {lead_id, manager_id, result, transcript?, amount?}
  GET  /crm_bridge/v2/sync_manager/{manager_id}
  POST /crm_bridge/v2/map_to_training    {lead, manager_id}
  POST /crm_bridge/v2/webhook            {event, payload}
  GET  /crm_bridge/v2/lead/{lead_id}

Интеграции (используются если доступны):
  • modules.dialog_memory.v1 (история, баллы, ошибки)
  • modules.edu_lessons.v1 (рекомендации на базе ошибок)
  • modules.sales_commission.v1 (опционально: расчёт дохода после закрытия сделки)

Формат данных /data/leads.json — мок-хранилище, можно переподключить к реальной CRM.
