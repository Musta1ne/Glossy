"""
Módulo de Speech-to-Text usando OpenAI Whisper (local, sin internet).
Modelo 'base' — buen balance velocidad/precisión para comandos cortos.
"""

import io
import whisper
import numpy as np

_model = None


def _get_model():
    global _model
    if _model is None:
        print("[STT] Cargando modelo Whisper 'base'...")
        _model = whisper.load_model("base")
        print("[STT] Modelo listo.")
    return _model


def transcribe_audio(audio_buffer: io.BytesIO) -> str:
    """
    Transcribe un buffer de audio WAV a texto en español.
    
    Args:
        audio_buffer: BytesIO con el audio en formato WAV 16kHz mono
    
    Returns:
        Texto transcripto (string)
    """
    model = _get_model()

    # Whisper acepta archivos o arrays numpy. Usamos el buffer directo.
    audio_buffer.seek(0)

    # Leer el WAV y convertir a float32 normalizado
    import wave
    with wave.open(audio_buffer, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio_array = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

    result = model.transcribe(
        audio_array,
        language="es",          # Forzar español
        task="transcribe",
        fp16=False,              # Usar float32 (más compatible con CPU)
        temperature=0.0,         # Más determinístico para comandos
        condition_on_previous_text=False,
    )

    text = result["text"].strip()
    return text
