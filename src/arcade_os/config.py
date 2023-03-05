from enum import Enum, auto


FULLSCREEN = False
SHOW_MOUSE = False
SCREEN_TITLE = "Starting Template"
SPLASH_SCREEN_TIME_DELAY = 1.0
SNES9X_EMULATOR_PATH = "flatpak run com.snes9x.Snes9x"
CONTROLLER_JSON_FILENAME = "controllers.json"


class GameTypes(Enum):
    PYTHON = auto()
    SNES = auto()
