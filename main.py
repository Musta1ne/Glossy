"""
Glossy - Asistente de voz para Windows
Ejecutar: python main.py
"""

import time
import threading
import sys
from wake_word import WakeWordDetector
from stt import transcribe_audio
from parser import parse_command
from tts import speak
from actions import execute_action


def on_wake_word_detected():
    """Callback que se ejecuta cuando se detecta 'glossy' o 'hey glossy'."""
    speak("Sí?")
    print("\n[Glossy] Wake word detectada! Escuchando comando...")

    audio_data = record_command()
    if audio_data is None:
        speak("No escuché nada.")
        return

    print("[Glossy] Transcribiendo...")
    text = transcribe_audio(audio_data)
    if not text or len(text.strip()) < 2:
        speak("No entendí el comando.")
        return

    print(f"[Glossy] Escuché: '{text}'")

    print("[Glossy] Interpretando con Ollama...")
    action = parse_command(text)
    if action is None:
        speak("No supe qué hacer con eso.")
        return

    print(f"[Glossy] Acción: {action}")
    execute_action(action)


def record_command():
    """Graba audio del micrófono por hasta 5 segundos."""
    import pyaudio
    import wave
    import io
    import numpy as np

    RATE = 16000
    CHUNK = 1024
    MAX_SECONDS = 5
    SILENCE_THRESHOLD = 500
    SILENCE_CHUNKS = 20  # ~1.3 segundos de silencio para cortar

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("[Glossy] Grabando... (hablá ahora)")
    frames = []
    silence_count = 0
    started_speaking = False

    for _ in range(int(RATE / CHUNK * MAX_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        amplitude = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(amplitude.astype(np.float32) ** 2))

        if rms > SILENCE_THRESHOLD:
            started_speaking = True
            silence_count = 0
        elif started_speaking:
            silence_count += 1
            if silence_count > SILENCE_CHUNKS:
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    if not started_speaking:
        return None

    # Convertir a bytes WAV en memoria
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    buf.seek(0)
    return buf


def main():
    print("=" * 50)
    print("  Glossy - Asistente de voz")
    print("  Decí 'glossy' o 'hey glossy' para activar")
    print("  Ctrl+C para salir")
    print("=" * 50)

    detector = WakeWordDetector(callback=on_wake_word_detected)

    try:
        detector.start()
        print("[Glossy] Escuchando wake word...")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[Glossy] Cerrando...")
        detector.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
