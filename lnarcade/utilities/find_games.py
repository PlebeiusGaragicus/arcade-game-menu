import os
import json
import logging
logger = logging.getLogger("lnarcade")

from lnarcade.config import APP_FOLDER
from lnarcade.views.error import show_error

def find_apps() -> list:
    home_folder = os.path.expanduser("~")
    arcade_apps_folder = os.path.join(home_folder, APP_FOLDER)
    if not os.path.exists(arcade_apps_folder):
        logger.critical(f"Could not find apps folder: {arcade_apps_folder}")
        show_error(f"Could not find apps folder: {arcade_apps_folder}")
        return [] # execution shouldn't reach this point

    return [f.path for f in os.scandir(arcade_apps_folder) if f.is_dir()]

def get_app_manifests() -> dict:
    games = find_apps()
    manifest_data = {}
    for game in games:
        manifest_path = os.path.join(game, "manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path) as f:
                    manifest_data[os.path.basename(game)] = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding manifest file {manifest_path}: {e}")
                continue

    return manifest_data
