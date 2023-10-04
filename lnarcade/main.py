import os
import logging
import dotenv

from lnarcade.version import VERSION
from lnarcade.logger import setup_logging


def main():
    dotenv.load_dotenv()

    setup_logging()
    logger = logging.getLogger("nospy")

    print(f"\n====================\n")
    print(f"Version {VERSION}")
    print(f"\n====================\n")
    if os.getenv("DEBUG"):
        print(f"DEBUG MODE IS ENABLED!")
        print(f"Password: {os.getenv('PASSWORD')}")

    logger.info("Hello, world!")
