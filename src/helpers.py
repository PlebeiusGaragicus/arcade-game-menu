import subprocess
import logging

import arcade

from src.config import GameTypes, SCREEN_TITLE, SNES9X_EMULATOR_PATH
from .views.SplashScreen import SplashScreen



def create_window(fullscreen: bool = False):
    # mouse_cursor_image = arcade.load_texture("assets/fire.png")
    # cursor = ImageMouseCursor(mouse_cursor_image, 0, 0)

    width, height = arcade.get_display_size()

    if fullscreen:
        window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
    else:
        window = arcade.Window(width=width, height=height, title=SCREEN_TITLE)

    view = SplashScreen()
    window.show_view(view)
    window.set_mouse_visible(False)
    arcade.run()



def launch_game(game: str):
        # NOTE: we can't do this here, we need to do it in the main thread
        # arcade.get_window().minimize()

        if game['type'] == GameTypes.PYTHON:
            cmd = f"{game['path']}/run"
            logging.debug(f"{cmd=}")
        elif game['type'] == GameTypes.SNES:
            cmd = SNES9X_EMULATOR_PATH + " \"" + game['path'] + "/" + game['name'] + ".zip\""
            # I CAN ONLY TEST THIS ON A DEBIAN MACHINE WITH SNES9X INSTALLED
            logging.debug(f"{cmd=}")
            return

        process = subprocess.Popen(args="", executable=cmd , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        logging.debug(f"{output=}")
        logging.debug(f"{error=}")
