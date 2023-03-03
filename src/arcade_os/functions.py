import os
import subprocess
import logging


from arcade_os.app import app
from arcade_os.config import SNES9X_EMULATOR_PATH, GameTypes
from arcade_os.input import SNESButton, N64Button, DragonRiseButton


### LAUNCH
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



def search_for_games():

    game_folder = app.get_instance().game_folder

    games = []
    for file_name in os.listdir(game_folder):
        logging.debug(f"{file_name=}")

        # if folder is ".DS_Store", skip it
        if file_name.startswith("."):
            logging.debug("skipping dot file")
            continue

        # check if file is a directory
        if os.path.isdir(os.path.join(game_folder, file_name)):
            logging.debug("This is a directory...")

            # if there is a folder named 'src' inside this directory
            if os.path.isdir(os.path.join(game_folder, file_name, "src")):
                type = GameTypes.PYTHON

            # else, if there is a .zip file inside this directory
            else:
                # TODO: I NEED TO HANDLE MORE THAN TWO TYPES... FIX THIS
                type = GameTypes.SNES

            logging.debug(f"found a game: {file_name} at '{os.path.join(game_folder, file_name)}' of type {type}")
            games.append({
                    "name": file_name,
                    "path": os.path.join(game_folder, file_name),
                    "type": type}
                )
        else:
            logging.debug("skipping this file...")

    logging.debug(games)
    return games
