import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, field

import logging
logger = logging.getLogger("nospy")



DATA_DIR = str(Path.home() / ".config/lnarcade")
CONFIG_FILENAME = f"{os.getenv('NOSPY_USER', 'default')}.json"


from lnarcade.models import Singleton



@dataclass
class Config(Singleton):
    state: dict = field(default_factory=dict)

    def __post_init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        # Parse config
        self.config_path = os.path.join(DATA_DIR, CONFIG_FILENAME)
        # NOTE: There is no reason to save an empty config file... also, we can't do this inside __init__ because self.state isn't set yet
        # if not os.path.exists(config_path):
        #     logging.warn(f"Config file not found. Creating a new one: {config_path}")
        #     self.save_config(config_path)
        # else:
        #     self.load_config(config_path)

        self.load_config()

    
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
