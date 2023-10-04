import os
import threading
import logging
import dotenv

# from lnarcade.version import VERSION
from lnarcade.logger import setup_logging
from lnarcade.config import Config
from lnarcade.models.menusystem import MenuSystem

def print_preamble():
    import pkg_resources
    version = pkg_resources.get_distribution("lightning_arcade_system").version

    print(f"\n====================\n")
    print(f"Version {version}")
    print(f"\n====================\n")
    if os.getenv("DEBUG"):
        print(f"DEBUG MODE IS ENABLED!")
        print(f"Password: {os.getenv('PASSWORD')}")


def main():
    # load environment variables
    if dotenv.load_dotenv() == False:
        # TODO: should I make this a critical error?
        print("WARNING!!!  No .env file found!!!")
        exit(1)

    # setup logging
    setup_logging()
    logger = logging.getLogger("lnarcade")
    logging.getLogger("arcade").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.INFO)

    print_preamble()

    # load config file
    relays = Config.get_instance().relays
    if relays == {}:
        logger.info("No relays saved.")
    print(relays)

    MenuSystem.get_instance().start()
