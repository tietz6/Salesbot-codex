
Place this into salesbot/integrations/patch_v3

This pack provides:
- Unified HTTP client (timeouts, JSON, headers)
- Simple .env loader and getter
- Retry decorator with exponential backoff
- Version stamp to track deployments

Recommended env (.env or OS env):
  HTTP_TIMEOUT=15
  HTTP_RETRIES=3
