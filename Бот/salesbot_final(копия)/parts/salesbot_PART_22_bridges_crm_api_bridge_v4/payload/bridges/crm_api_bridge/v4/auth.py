
import os, time

class CRMAuth:
    def __init__(self, token: str|None=None):
        self._token = token or os.getenv("CRM_API_TOKEN","")
        self._exp = time.time() + 24*3600

    def headers(self)->dict:
        return {"Authorization": f"Bearer {self._token}"} if self._token else {}
