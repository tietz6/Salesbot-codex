
PART 20 — Voice Gateway bindings (Variant A: Local VoicePipeline)
---------------------------------------------------------------
Эндпоинты:
  GET  /api/voice/v1/health
  POST /api/voice/v1/transcribe        (file: audio/*)
  POST /api/voice/v1/speak             (form/text)
  POST /api/voice/v1/ask_llm           (form/text, form/system_prompt?)
  POST /api/voice/v1/run               (file: audio/*, form/system_prompt?)

Требования:
  - core/voice_gateway/v1
  - ENV: DEEPSEEK_API_KEY, ASSEMBLYAI_API_KEY (если используешь AssemblyAI), TTS_PROVIDER=pyttsx3 (по умолчанию)

Примечание:
  В ответах /speak и /run поле tts_audio_b64 — это base64 кодек WAV.
