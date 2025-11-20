
Place into salesbot/apps/mini_webkit/v2

What it gives:
  - Minimal FastAPI web app mounted at /mini
  - UI with /mini/ (index), /mini/health
  - Simple API endpoints that can call CRM bridge and Voice Gateway (optional)
  - Templated UI (Jinja2) + static assets

Env (optional):
  MINI_TITLE="Salesbot Mini WebKit"
  CRM_API_BASE=...
  CRM_API_TOKEN=...
  DEEPSEEK_API_KEY=...
