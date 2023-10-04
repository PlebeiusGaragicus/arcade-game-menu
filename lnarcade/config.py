import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field

import logging
logger = logging.getLogger("lnarcade")


from lnarcade.models.singleton import SingletonDataclass


MY_DIR = os.path.dirname(os.path.realpath(__file__))    # Path: lnarcade
DATA_DIR = str(Path.home() / ".config")
CONFIG_FILENAME = "lnarcade.json"
APP_FOLDER = "arcade-apps" # located in the home folder

# FULLSCREEN = True
FULLSCREEN = False
SHOW_MOUSE = False
SCREEN_TITLE = "Starting Template"
SPLASH_SCREEN_TIME_DELAY = 0.5
SNES9X_EMULATOR_PATH = "flatpak run com.snes9x.Snes9x"





@dataclass
class Config(SingletonDataclass):
    state: dict = field(default_factory=dict)

    def __post_init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.config_path = os.path.join(DATA_DIR, CONFIG_FILENAME)
        self.load_config()


    @property
    def relays(self) -> dict:
        return self.state.get("relays", {})

    def add_relay(self, addr, policy) -> None:
        if "relays" not in self.state:
            self.state["relays"] = {}
        self.state["relays"][addr] = policy


    def remove_relay(self, addr) -> bool:
        if "relays" in self.state and addr in self.state["relays"]:
            del self.state["relays"][addr]
            return True
        else:
            return False

    def clear_relays(self) -> None:
        self.state["relays"] = {}


    def save_config(self):
        """Save the config file."""

        # data_dir = str(Path.home() / DATA_DIR)
        os.makedirs(DATA_DIR, exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(self.state, f, indent=4)

        logger.debug(f"Saving the current config to file: {self.config_path}")
        # logger.debug(f"Config: {self.state}")


    def load_config(self):
        """Initialize the config file."""
        logger.debug(f"Loading config file: {self.config_path}")

        if not os.path.exists(self.config_path):
            # logger.warn(f"Config file not found.")
            self.state = {} # Set the state to an empty dictionary
            return

        # TODO: I'm not sure this is even needed...
        if os.path.getsize(self.config_path) == 0:
            # logger.warn(f"Config file is empty.")
            self.state = {}  # Set the state to an empty dictionary
            return

        with open(self.config_path, "r") as f:
            try:
                self.state = json.load(f)
                # logger.debug(f"Config: {self.state}")
            except json.JSONDecodeError as e:
                logger.critical(f"Can't parse config file. Ensure the file is properly formatted JSON. {self.config_path}: {str(e)}")
                sys.exit(1)
