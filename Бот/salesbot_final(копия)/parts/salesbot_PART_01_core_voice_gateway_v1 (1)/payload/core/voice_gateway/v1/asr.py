
import os
from .exceptions import NotConfigured, ProviderError

class ASR:
    def __init__(self, provider: str|None=None, api_key: str|None=None):
        self.provider = provider or os.getenv("ASR_PROVIDER","assemblyai")
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
    def transcribe(self, audio_bytes: bytes, language: str="auto")->str:
        if not audio_bytes:
            raise ProviderError("ASR: empty audio")
        if self.provider.lower()=="assemblyai":
            if not self.api_key:
                raise NotConfigured("ASSEMBLYAI_API_KEY not set")
            # Lazy import to avoid hard dep if user chooses another provider
            try:
                import assemblyai as aai
            except Exception as e:
                raise ProviderError(f"assemblyai not installed: {e}")
            aai.settings.api_key = self.api_key
            transcriber = aai.Transcriber()
            result = transcriber.transcribe(audio_bytes)
            return result.text or ""
        # fallback simple "fake" decoder for wav/pcm16 -> returns marker to avoid silent stubs
        try:
            import wave, io
            wave.open(io.BytesIO(audio_bytes),"rb")
            return "[local-asr: audio detected]"
        except Exception:
            raise ProviderError("ASR: no supported provider and no wav")
