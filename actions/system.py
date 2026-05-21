"""
Controlador del sistema para Windows.
- Volumen del sistema vía teclas multimedia (pynput)
- Apertura de aplicaciones vía subprocess
"""

import subprocess
from tts import speak
from pynput.keyboard import Key, Controller

keyboard = Controller()

APP_MAP = {
    "spotify":      "spotify.exe",
    "chrome":       "chrome.exe",
    "google chrome":"chrome.exe",
    "firefox":      "firefox.exe",
    "notepad":      "notepad.exe",
    "bloc de notas":"notepad.exe",
    "explorer":     "explorer.exe",
    "calculadora":  "calc.exe",
    "calculator":   "calc.exe",
    "word":         "winword.exe",
    "excel":        "excel.exe",
    "vscode":       "code.exe",
    "visual studio code": "code.exe",
    "discord":      "discord.exe",
    "telegram":     "telegram.exe",
    "whatsapp":     "whatsapp.exe",
}


class SystemController:
    def volume_up(self, amount: int = 10):
        steps = max(1, amount // 2)
        for _ in range(steps):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
        speak("Volumen del sistema subido.")

    def volume_down(self, amount: int = 10):
        steps = max(1, amount // 2)
        for _ in range(steps):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
        speak("Volumen del sistema bajado.")

    def mute(self):
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
        speak("Sistema silenciado.")

    def unmute(self):
        keyboard.press(Key.media_volume_mute)
        keyboard.release(Key.media_volume_mute)
        speak("Silencio quitado.")

    def open_app(self, app_name: str):
        if not app_name:
            speak("No sé qué aplicación abrir.")
            return
        app_key = app_name.lower().strip()
        executable = APP_MAP.get(app_key)
        if executable:
            try:
                subprocess.Popen(executable, shell=True)
                speak(f"Abriendo {app_name}.")
                return
            except Exception as e:
                print(f"[System] Error abriendo {executable}: {e}")
        try:
            subprocess.Popen(app_name, shell=True)
            speak(f"Abriendo {app_name}.")
        except FileNotFoundError:
            speak(f"No encontré la aplicación {app_name}.")
        except Exception as e:
            speak(f"No pude abrir {app_name}.")
            print(f"[System] Error: {e}")