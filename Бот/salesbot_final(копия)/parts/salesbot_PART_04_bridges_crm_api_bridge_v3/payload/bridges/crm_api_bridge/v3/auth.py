
import os, time
from typing import Optional

class CRMAuth:
    def __init__(self, token: Optional[str]=None):
        self._token = token or os.getenv("CRM_API_TOKEN","")
        self._exp = time.time() + 24*3600  # fake TTL for static token

    @property
    def token(self)->str:
        if time.time() >= self._exp:
            # if refresh is needed, implement here
            self._exp = time.time() + 24*3600
        return self._token

    def headers(self)->dict:
        t = self.token
        return {"Authorization": f"Bearer {t}"} if t else {}
