import sys
import os

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#Setting.py
WIDTH = 800
HEIGHT = 600
# Timers
POMODORO_MINS = 25
SHORT_BREAK_MINS = 5
LONG_BREAK_MINS = 10

# Fuentes
FONT_FAMILY = "Space Grotesk"
TIMER_SIZE = 100
MAIN_SIZE = 16

# File Paths
FONT_PATH = "font/SpaceGrotesk-VariableFont_wght.ttf"
SETTINGS_ICON_PATH = "images/settings_icon.png"
RESET_ICON_PATH = "images/reset_icon.png"

TEXT_COLOR = 'White'
TIMER_COLOR = "White"
BG_COLOR = "#FBE8E6"


SETTINGS_ICON_PATH = "images/settings_icon.png"
RESET_ICON_PATH = "images/reset_icon.png"

STYLE_ACTIVO ={
    "fg_color": "white",
    "text_color": "#6D4C6C",
    "border_width": 0,
    "hover": False
}

STYLE_INACTIVO = {
    "fg_color": "transparent",
    "border_width": 2,
    "border_color": "#6D4C6C",
    "text_color": ("#6D4C6C", "#FDF5F5")

}
