import subprocess
import logging

from src.app import SNES9X_EMULATOR_PATH

from enum import Enum, auto
class GameTypes(Enum):
    PYTHON = auto()
    SNES = auto()



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
