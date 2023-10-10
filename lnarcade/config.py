import os
from pathlib import Path

import logging
logger = logging.getLogger()



MY_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = str(Path.home() / ".config")
DOT_ENV_PATH = os.path.join(DATA_DIR, ".lnarcade")

# located in the home folder
APP_FOLDER = "arcade-apps"

SHOW_MOUSE = False
SCREEN_TITLE = "Lightning Arcade"


#TODO - maybe each app should play a gif instead of display a static image
# AFK_SCROLL_TIME = 20  # seconds - the time it takes to scroll through the menu when AFK


def create_default_dot_env():
    print("creating default .env file in {}".format(DOT_ENV_PATH))

    with open(DOT_ENV_PATH, "w") as f:
        env = "DEBUG=False\n"
        env += "FREE_PLAY=True\n"
        env += "SNES9X_EMULATOR_PATH='flatpak run com.snes9x.Snes9x'"

        f.write( env )

