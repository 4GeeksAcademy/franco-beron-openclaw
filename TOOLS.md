# TOOLS.md - Local Notes

## TTS (Text-to-Speech)

**Voz por defecto:** Daniela (Piper, argentina/rioplatense)
- Modelo: `es_AR-daniela-high.onnx` (114MB)
- Config: `noise_scale=0.8`, `noise_w=1.0`, `length_scale=0.9`
- Script: `/root/.openclaw/workspace/tts.py` (usar este siempre)

**Flujo para responder con audio:**
1. Generar WAV con Python/piper
2. Convertir a OGG con ffmpeg
3. Enviar con sendVoice via Telegram Bot API

**Flujo para recibir audios:**
1. ffmpeg convierte inbound .ogg → WAV 16kHz
2. whisper tiny transcribe
3. Responder normalmente

## Telegram

- Bot: @fraberon_bot (7990245507)
- Token guardado en openclaw.json
- Chat ID: 8805705179 (Franco)