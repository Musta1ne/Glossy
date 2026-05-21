"""
Módulo de Text-to-Speech usando pyttsx3 (offline, sin internet).
"""

import pyttsx3
import threading

_engine = None
_lock = threading.Lock()


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Configurar voz en español si está disponible
        voices = _engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                _engine.setProperty('voice', voice.id)
                break
        _engine.setProperty('rate', 160)   # velocidad de habla
        _engine.setProperty('volume', 0.9)
    return _engine


def speak(text: str):
    """
    Hace que Glossy hable el texto dado.
    Thread-safe, bloqueante hasta terminar de hablar.
    
    Args:
        text: Texto a vocalizar
    """
    print(f"[TTS] '{text}'")
    with _lock:
        engine = _get_engine()
        engine.say(text)
        engine.runAndWait()
