"""
Controlador de Spotify usando la API oficial (spotipy).

Configuración necesaria (en config.py o variables de entorno):
  SPOTIPY_CLIENT_ID     → de https://developer.spotify.com/dashboard
  SPOTIPY_CLIENT_SECRET
  SPOTIPY_REDIRECT_URI  → http://localhost:8888/callback

La primera vez que corras esto, va a abrir el navegador para autenticarte.
El token se guarda en .spotify_cache y se renueva automáticamente.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tts import speak
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

SCOPE = " ".join([
    "user-modify-playback-state",
    "user-read-playback-state",
    "user-read-currently-playing",
])


class SpotifyController:
    def __init__(self):
        self._sp = None

    def _get_client(self) -> spotipy.Spotify:
        if self._sp is None:
            self._sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET,
                    redirect_uri=SPOTIFY_REDIRECT_URI,
                    scope=SCOPE,
                    cache_path=".spotify_cache",
                    open_browser=True,
                )
            )
        return self._sp

    def _get_active_device_id(self) -> str | None:
        """Retorna el ID del dispositivo activo de Spotify."""
        sp = self._get_client()
        devices = sp.devices()
        active = [d for d in devices.get("devices", []) if d["is_active"]]
        if active:
            return active[0]["id"]
        # Si ninguno está activo, usar el primero disponible
        all_devices = devices.get("devices", [])
        if all_devices:
            return all_devices[0]["id"]
        return None

    def play(self):
        sp = self._get_client()
        sp.start_playback()
        speak("Reproduciendo.")

    def pause(self):
        sp = self._get_client()
        sp.pause_playback()
        speak("Pausado.")

    def next_track(self):
        sp = self._get_client()
        sp.next_track()
        speak("Siguiente.")

    def previous_track(self):
        sp = self._get_client()
        sp.previous_track()
        speak("Anterior.")

    def volume_up(self, amount: int = 10):
        sp = self._get_client()
        current = sp.current_playback()
        if current and current.get("device"):
            current_vol = current["device"]["volume_percent"]
            new_vol = min(100, current_vol + amount)
            sp.volume(new_vol)
            speak(f"Volumen al {new_vol} por ciento.")
        else:
            speak("No encontré un dispositivo de Spotify activo.")

    def volume_down(self, amount: int = 10):
        sp = self._get_client()
        current = sp.current_playback()
        if current and current.get("device"):
            current_vol = current["device"]["volume_percent"]
            new_vol = max(0, current_vol - amount)
            sp.volume(new_vol)
            speak(f"Volumen al {new_vol} por ciento.")
        else:
            speak("No encontré un dispositivo de Spotify activo.")

    def search_and_play(self, query: str):
        if not query:
            speak("No entendí qué querés escuchar.")
            return
        sp = self._get_client()
        results = sp.search(q=query, type="track,artist,album", limit=1)

        # Intentar reproducir artista primero, luego track
        device_id = self._get_active_device_id()

        artists = results.get("artists", {}).get("items", [])
        if artists:
            artist = artists[0]
            sp.start_playback(device_id=device_id, context_uri=artist["uri"])
            speak(f"Poniendo {artist['name']}.")
            return

        tracks = results.get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            sp.start_playback(device_id=device_id, uris=[track["uri"]])
            speak(f"Poniendo {track['name']} de {track['artists'][0]['name']}.")
            return

        speak(f"No encontré nada para {query}.")
