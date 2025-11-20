
import json, requests
from .utils import integration_result

class ExternalAPI:
    def fetch(self, url: str, params: dict=None):
        try:
            r = requests.get(url, params=params or {})
            return integration_result(True, r.json())
        except Exception as e:
            return integration_result(False, error=str(e))
