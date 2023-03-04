from enum import Enum, auto


FULLSCREEN = False
SHOW_MOUSE = False
SCREEN_TITLE = "Starting Template"
SPLASH_SCREEN_TIME_DELAY = 0.5
SNES9X_EMULATOR_PATH = "flatpak run com.snes9x.Snes9x"



class GameTypes(Enum):
    PYTHON = auto()
    SNES = auto()
