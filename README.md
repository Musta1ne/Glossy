# Glossy — Asistente de voz para Windows

---

## Requisitos previos

- Python 3.10 o superior
- [Ollama](https://ollama.com) instalado y corriendo
- Cuenta de Spotify Premium

---

## Instalación paso a paso

### 1. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

> Si falla `pyaudio` en Windows, instalalo con:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### 2. Instalar y configurar Ollama

1. Descargá Ollama desde https://ollama.com
2. Instalalo y abrí una terminal
3. Descargá el modelo:
   ```bash
   ollama pull llama3.2
   ```
4. Asegurate de que esté corriendo:
   ```bash
   ollama serve
   ```

### 3. Configurar Spotify

1. Ir a https://developer.spotify.com/dashboard
2. Hacer clic en **"Create app"**
3. Nombre: `Glossy` (o el que quieras)
4. En **"Redirect URIs"** agregar: `http://localhost:8888/callback`
5. Copiar el **Client ID** y el **Client Secret**
6. Abrir `config.py` y pegarlo:
   ```python
   SPOTIFY_CLIENT_ID     = "tu_client_id"
   SPOTIFY_CLIENT_SECRET = "tu_client_secret"
   ```

### 4. Primera ejecución

```bash
python main.py
```

La primera vez va a abrir el navegador para que autorices Glossy a controlar Spotify.
Después de aceptar, el token se guarda en `.spotify_cache` y no te lo vuelve a pedir.

---

## Uso

1. Corré `python main.py`
2. Decí **"hey glossy"** (o cualquier frase con "glossy" al final)
3. Glossy responde "Sí?" — ahí hablás tu comando
4. Ejemplos de comandos:

| Decís | Acción |
|-------|--------|
| "abrí Spotify" | Abre la app de Spotify |
| "siguiente canción" | Pasa a la siguiente |
| "anterior" | Vuelve a la anterior |
| "pausá" / "pausá la música" | Pausa Spotify |
| "seguí" / "reproducí" | Reanuda |
| "subí el volumen" | +10% volumen Spotify |
| "bajá bastante el volumen" | -10% volumen Spotify |
| "subí el volumen del sistema" | +10% volumen Windows |
| "poneme algo de Radiohead" | Busca y reproduce |
| "abrí Chrome" | Abre Google Chrome |
| "silenciá el sistema" | Mute Windows |

---

## Personalización

### Cambiar el modelo de Ollama

En `config.py`:
```python
OLLAMA_MODEL = "phi3"   # más liviano
# o
OLLAMA_MODEL = "llama3.1"  # más preciso
```

### Ajustar sensibilidad de la wake word

En `config.py`:
```python
WAKE_WORD_THRESHOLD = 0.5  # bajar si no detecta, subir si hay falsos positivos
```

### Agregar nuevas apps al mapa

En `actions/system.py`, en el diccionario `APP_MAP`:
```python
"mi app": "miapp.exe",
```

### Agregar nuevas acciones

1. Agregar la acción al prompt en `parser.py`
2. Crear la función en `actions/spotify.py` o `actions/system.py`
3. Registrarla en `actions/__init__.py` en `_ACTION_MAP`

---

## Troubleshooting

**"Ollama no está corriendo"**
→ Abrí una terminal y ejecutá `ollama serve`

**La wake word no detecta**
→ Bajá el `WAKE_WORD_THRESHOLD` en `config.py` (ej: `0.3`)

**Spotify da error de autenticación**
→ Borrá el archivo `.spotify_cache` y volvé a correr

**No hay sonido en TTS**
→ Verificá que `pyttsx3` esté instalado y que Windows tenga voces instaladas

---

## Estructura del proyecto

```
glossy/
├── main.py              # Entry point — loop principal
├── wake_word.py         # Detección de "hey glossy"
├── stt.py               # Whisper — voz a texto
├── parser.py            # Ollama — interpreta el comando
├── tts.py               # pyttsx3 — respuesta de voz
├── config.py            # ← Tus credenciales van acá
├── requirements.txt
└── actions/
    ├── __init__.py      # Router de acciones
    ├── spotify.py       # Control de Spotify
    └── system.py        # Control del sistema Windows
```
