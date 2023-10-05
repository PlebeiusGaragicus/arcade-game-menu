import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field

import logging
logger = logging.getLogger()



MY_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = str(Path.home() / ".config")
CONFIG_FILENAME = "lnarcade.json"

# located in the home folder
APP_FOLDER = "arcade-apps"

FREE_PLAY = True
SHOW_MOUSE = False
SCREEN_TITLE = "Lightning Arcade"
SPLASH_SCREEN_TIME_DELAY = 0.5

# SNES9X_EMULATOR_PATH = "flatpak run com.snes9x.Snes9x"

@dataclass
class Config():
    state: dict = field(default_factory=dict)

    def __post_init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.config_path = os.path.join(DATA_DIR, CONFIG_FILENAME)
        self.load_config()





    #################################################
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
    ###################################################



    def get(self, key, default=None):
        return self.state.get(key, default)

    def set(self, key, value):
        self.state[key] = value

    def set_empty_state(self):
        self.state = {}
        self.state['SNES_EMULATOR_CMD'] = "flatpak run com.snes9x.Snes9x"
        self.save_config()


    def save_config(self):
        """Save the config file."""

        # data_dir = str(Path.home() / DATA_DIR)
        os.makedirs(DATA_DIR, exist_ok=True)

        with open(self.config_path, "w") as f:
            json.dump(self.state, f, indent=4)

        logger.debug(f"Saving config to file: {self.config_path}")


    def load_config(self):
        """Initialize the config file."""
        logger.debug(f"Loading config file: {self.config_path}")

        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found.")
            # self.state = {} # Set the state to an empty dictionary
            self.set_empty_state()
            return

        # empty config file (will cause a JSONDecodeError)
        if os.path.getsize(self.config_path) == 0:
            logger.warning(f"Config file is empty.")
            # self.state = {}  # Set the state to an empty dictionary
            self.set_empty_state()
            return

        with open(self.config_path, "r") as f:
            try:
                self.state = json.load(f)
            except json.JSONDecodeError as e:
                # TODO: I could just proceed with an empty config state after I show an error message (but how do I show an error message before anything has been initialized?)
                logger.error(f"Can't parse config file. Ensure the file is properly formatted JSON. {self.config_path}: {str(e)}")
                exit(1)
