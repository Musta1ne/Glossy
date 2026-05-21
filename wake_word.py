"""
Módulo de detección de wake word usando openWakeWord.
Detecta 'hey mycroft' como proxy, o un modelo personalizado si lo tenés.

NOTA: openWakeWord viene con varios modelos incluidos.
Para una wake word personalizada "glossy" podés entrenar en:
https://github.com/dscripka/openWakeWord#training-new-models
"""

import threading
import numpy as np
import pyaudio
from openwakeword.model import Model


# Modelos disponibles en openWakeWord (sin instalación extra):
# "alexa", "hey_mycroft", "hey_jarvis", "hey_rhasspy", "ok_nabu"
# Para "glossy" necesitás entrenar un modelo propio.
# Por defecto usamos "hey_jarvis" que suena similar a "hey glossy".
WAKE_WORD_MODEL = "hey_jarvis"

# Sensibilidad (0.0 a 1.0) — bajar si hay muchos falsos positivos
THRESHOLD = 0.5

RATE = 16000
CHUNK = 1280  # openWakeWord espera chunks de 80ms a 16kHz


class WakeWordDetector:
    def __init__(self, callback):
        self.callback = callback
        self._running = False
        self._thread = None
        self._stream = None
        self._audio = None
        self.model = None

    def _load_model(self):
        print(f"[WakeWord] Cargando modelo '{WAKE_WORD_MODEL}'...")
        self.model = Model(
            wakeword_models=[WAKE_WORD_MODEL],
            enable_speex_noise_suppression=False,
            inference_framework="onnx",
        )
        print("[WakeWord] Modelo listo.")

    def _listen_loop(self):
        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            input_device_index=1,
            frames_per_buffer=CHUNK,
        )

        cooldown = 0  # evitar activaciones múltiples seguidas

        while self._running:
            data = self._stream.read(CHUNK, exception_on_overflow=False)
            audio_array = np.frombuffer(data, dtype=np.int16)

            prediction = self.model.predict(audio_array)

            if cooldown > 0:
                cooldown -= 1
                continue

            score = prediction.get(WAKE_WORD_MODEL, 0)
            if score >= THRESHOLD:
                cooldown = 30  # ~2.4 segundos de cooldown
                # Ejecutar callback en hilo separado para no bloquear el listener
                threading.Thread(target=self.callback, daemon=True).start()

        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()

    def start(self):
        self._load_model()
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
