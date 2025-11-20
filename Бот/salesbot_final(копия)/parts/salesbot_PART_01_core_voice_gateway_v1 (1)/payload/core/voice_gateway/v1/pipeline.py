
from .asr import ASR
from .tts import TTS
from .deepseek_bridge import DeepSeekChat

class VoicePipeline:
    def __init__(self):
        self.asr = ASR()
        self.tts = TTS()
        self.llm = DeepSeekChat()
    def run(self, audio_bytes: bytes, system_prompt: str="You are a helpful sales coach."):
        text = self.asr.transcribe(audio_bytes)
        reply = self.llm.chat([
            {"role":"system","content":system_prompt},
            {"role":"user","content":text or "[no speech recognized]"}
        ])
        audio = self.tts.synthesize(reply)
        return {"asr_text": text, "reply_text": reply, "tts_audio_bytes": audio}
