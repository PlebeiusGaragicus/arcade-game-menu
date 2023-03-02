import sys
import logging

from src.config import FULLSCREEN
from src.helpers import create_window

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
         format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s")

    # logging.getLogger("arcade").setLevel(logging.INFO)
    logging.getLogger("arcade").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.INFO)

    # if no arguments are passed, show error
    if len(sys.argv) == 1:
        logging.critical("No game folder given - quitting")
        sys.exit(1)
    else:
        logging.debug(f"using supplied game folder: {sys.argv[1]}")

    create_window(FULLSCREEN)
