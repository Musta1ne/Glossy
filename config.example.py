"""
Configuración de Glossy.

ANTES DE CORRER:
1. Ir a https://developer.spotify.com/dashboard
2. Crear una app nueva
3. En "Edit Settings" agregar como Redirect URI: http://127.0.0.1:8888/callback
4. Copiar Client ID y Client Secret acá abajo
"""

# ─── Spotify ──────────────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID     = "TU_CLIENT_ID_AQUI"
SPOTIFY_CLIENT_SECRET = "TU_CLIENT_SECRET_AQUI"
SPOTIFY_REDIRECT_URI  = "http://127.0.0.1:8888/callback"

# ─── Ollama ───────────────────────────────────────────────────────────────────
# Modelo a usar. Asegurate de tenerlo descargado: ollama pull llama3.2
OLLAMA_MODEL = "llama3.2"
OLLAMA_URL   = "http://localhost:11434/api/generate"

# ─── Wake word ────────────────────────────────────────────────────────────────
# Sensibilidad de detección (0.0 - 1.0)
# Bajar si hay muchos falsos positivos, subir si no detecta bien
WAKE_WORD_THRESHOLD = 0.5
