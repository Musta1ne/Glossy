"""
Módulo de acciones de Glossy.
Rutea cada acción al ejecutor correspondiente.
"""

from .spotify import SpotifyController
from .system import SystemController
from tts import speak

_spotify = SpotifyController()
_system = SystemController()

# Mapeo de acción → función ejecutora
_ACTION_MAP = {
    # Spotify
    "spotify_play":         lambda p: _spotify.play(),
    "spotify_pause":        lambda p: _spotify.pause(),
    "spotify_next":         lambda p: _spotify.next_track(),
    "spotify_previous":     lambda p: _spotify.previous_track(),
    "spotify_volume_up":    lambda p: _spotify.volume_up(p.get("amount", 10)),
    "spotify_volume_down":  lambda p: _spotify.volume_down(p.get("amount", 10)),
    "spotify_search_play":  lambda p: _spotify.search_and_play(p.get("query", "")),

    # Sistema
    "system_open_app":      lambda p: _system.open_app(p.get("app_name", "")),
    "system_volume_up":     lambda p: _system.volume_up(p.get("amount", 10)),
    "system_volume_down":   lambda p: _system.volume_down(p.get("amount", 10)),
    "system_mute":          lambda p: _system.mute(),
    "system_unmute":        lambda p: _system.unmute(),
}


def execute_action(action_dict: dict):
    """
    Ejecuta la acción descripta en el dict.
    
    Args:
        action_dict: {"action": str, "params": dict}
    """
    action = action_dict.get("action")
    params = action_dict.get("params", {})

    handler = _ACTION_MAP.get(action)
    if handler is None:
        speak("No sé cómo hacer eso todavía.")
        print(f"[Actions] Acción no reconocida: '{action}'")
        return

    try:
        handler(params)
    except Exception as e:
        speak("Algo salió mal.")
        print(f"[Actions] ERROR ejecutando '{action}': {e}")
