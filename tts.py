#!/usr/bin/env python3
"""Generar audio con Daniela (Piper, argentina) y enviar por Telegram."""

import sys, json, wave, requests
from piper import PiperVoice

MODEL = '/tmp/piper_ar_daniela.onnx'
CONFIG = '/tmp/piper_ar_daniela.onnx.json'
CHAT_ID = '8805705179'

with open('/root/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
    TOKEN = cfg['channels']['telegram']['botToken']

def generar_y_enviar(texto):
    voice = PiperVoice.load(MODEL)
    audio_gen = voice.synthesize(texto)
    audio_data = bytearray()
    sr = None
    for chunk in audio_gen:
        audio_data.extend(chunk.audio_int16_bytes)
        if sr is None:
            sr = chunk.sample_rate

    wav_path = '/tmp/tts_output.wav'
    with wave.open(wav_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr or 22050)
        wf.writeframes(bytes(audio_data))

    ogg_path = '/tmp/tts_output.ogg'
    import subprocess
    subprocess.run(['ffmpeg', '-y', '-i', wav_path, '-acodec', 'libopus',
                    '-b:a', '24k', ogg_path], capture_output=True)

    with open(ogg_path, 'rb') as f:
        r = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendVoice',
                          data={'chat_id': CHAT_ID},
                          files={'voice': f})
    return r.json().get('ok', False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 tts.py 'texto a hablar'")
        sys.exit(1)
    ok = generar_y_enviar(' '.join(sys.argv[1:]))
    print('✅ Enviado' if ok else '❌ Error')