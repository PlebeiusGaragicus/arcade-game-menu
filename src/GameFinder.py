import os
import sys
import logging

from src.config import GameTypes

class GameFinder:
    def find_games():
        game_folder = sys.argv[1]
        logging.debug(f"{game_folder=}")

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
    