"""
Parser de comandos usando Ollama (LLM local).
Convierte lenguaje natural a acciones estructuradas.

Requiere Ollama corriendo en localhost:11434
Modelo recomendado: llama3.2 o phi3
  > ollama pull llama3.2
"""

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"  # Cambiá por el modelo que tengas instalado

SYSTEM_PROMPT = """Eres el parser de comandos del asistente de voz Glossy.
Tu trabajo es convertir comandos en lenguaje natural (en español) a JSON estructurado.

Acciones disponibles y sus parámetros:

SPOTIFY:
- spotify_play: reanudar reproducción
- spotify_pause: pausar
- spotify_next: siguiente canción
- spotify_previous: canción anterior
- spotify_volume_up: subir volumen de Spotify (amount: 10 por defecto)
- spotify_volume_down: bajar volumen de Spotify (amount: 10 por defecto)
- spotify_search_play: buscar y reproducir (query: "nombre artista/canción")

SISTEMA:
- system_open_app: abrir aplicación (app_name: nombre de la app)
- system_volume_up: subir volumen del sistema Windows (amount: 10) — SOLO si el usuario dice explícitamente "sistema" o "de la pc" o "de windows"
- system_volume_down: bajar volumen del sistema Windows (amount: 10) — SOLO si el usuario dice explícitamente "sistema" o "de la pc" o "de windows"
- system_mute: silenciar sistema
- system_unmute: quitar silencio

OTROS:
- unknown: no pude identificar la acción

Respondé SOLO con JSON válido, sin texto extra. Formato:
{"action": "nombre_accion", "params": {"clave": "valor"}}

Ejemplos:
- "abrí spotify" → {"action": "system_open_app", "params": {"app_name": "Spotify"}}
- "siguiente canción" → {"action": "spotify_next", "params": {}}
- "subí el volumen" → {"action": "spotify_volume_up", "params": {"amount": 10}}
- "bajá el volumen del sistema" → {"action": "system_volume_down", "params": {"amount": 10}}
- "poneme algo de Radiohead" → {"action": "spotify_search_play", "params": {"query": "Radiohead"}}
- "pausá" → {"action": "spotify_pause", "params": {}}
"""


def parse_command(text: str) -> dict | None:
    """
    Interpreta un comando de texto y retorna la acción a ejecutar.
    
    Args:
        text: Texto transcripto del usuario
    
    Returns:
        Dict con {"action": str, "params": dict} o None si hay error
    """
    prompt = f"Comando del usuario: \"{text}\""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "num_predict": 100,
                }
            },
            timeout=60,
        )
        response.raise_for_status()
        raw = response.json().get("message", {}).get("content", "").strip()

        # Limpiar posibles bloques de código markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)

        if "action" not in result:
            return None

        if result["action"] == "unknown":
            return None

        return result

    except requests.exceptions.ConnectionError:
        print("[Parser] ERROR: Ollama no está corriendo. Iniciá Ollama con: ollama serve")
        return None
    except json.JSONDecodeError as e:
        print(f"[Parser] ERROR al parsear JSON de Ollama: {e}")
        print(f"[Parser] Respuesta recibida: {raw!r}")
        return None
    except Exception as e:
        print(f"[Parser] ERROR inesperado: {e}")
        return None
