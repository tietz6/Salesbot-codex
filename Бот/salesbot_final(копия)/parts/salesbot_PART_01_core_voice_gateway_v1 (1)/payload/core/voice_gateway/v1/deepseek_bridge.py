
import os, json, urllib.request

class DeepSeekChat:
    def __init__(self, api_key: str|None=None, base_url: str|None=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL","https://api.deepseek.com/v1/chat/completions")
    def chat(self, messages, model="deepseek-chat", temperature=0.7)->str:
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY not set")
        body = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature
        }).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=body, method="POST")
        req.add_header("Content-Type","application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        # adapt to expected schema
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return str(data)
