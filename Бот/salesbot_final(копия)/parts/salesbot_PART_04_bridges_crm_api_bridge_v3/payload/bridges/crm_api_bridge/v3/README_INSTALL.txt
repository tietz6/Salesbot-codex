
Place into salesbot/bridges/crm_api_bridge/v3

What it gives:
  - Token auth (CRMAuth) with refresh support
  - CRMClient with simple methods: get_contact/upsert_contact/list_deals/create_deal/add_note
  - JSON-safe dataclasses for Contact/Deal/Note
  - HTTP via integrations/patch_v3.http_client (with retry/backoff)

Required env (.env / OS env):
  CRM_API_BASE=https://your-crm/api
  CRM_API_TOKEN=your-token    # static token or initial token
  CRM_API_TIMEOUT=20
  HTTP_TIMEOUT=15
  HTTP_RETRIES=3
