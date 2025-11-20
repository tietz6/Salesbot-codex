
import os
from .exceptions import NotConfigured, ProviderError

class TTS:
    def __init__(self, provider: str|None=None):
        self.provider = (provider or os.getenv("TTS_PROVIDER","pyttsx3")).lower()
    def synthesize(self, text: str)->bytes:
        if not text:
            return b""
        if self.provider=="pyttsx3":
            try:
                import pyttsx3, tempfile, wave, contextlib, os as _os
                engine = pyttsx3.init()
                tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                name = tmp.name; tmp.close()
                engine.save_to_file(text, name)
                engine.runAndWait()
                data = open(name,"rb").read()
                try: _os.remove(name)
                except: pass
                return data
            except Exception as e:
                raise ProviderError(f"pyttsx3 TTS failed: {e}")
        raise NotConfigured(f"TTS provider not configured: {self.provider}")
