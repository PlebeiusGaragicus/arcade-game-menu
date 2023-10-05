import os
import time
from dataclasses import dataclass
import subprocess
import logging
logger = logging.getLogger("lnarcade")

import arcade

from lnarcade.config import APP_FOLDER, MY_DIR, FULLSCREEN, FREE_PLAY
from lnarcade.utilities.find_games import get_app_manifests
from lnarcade.views.error import ErrorModalView

@dataclass
class MenuItem():
    def __init__(self, module_name: str, game_name: str, manifest_dict: dict, image_path: str):
        self.module_name = module_name
        self.game_name = game_name
        self.manifest_dict: dict = manifest_dict

        try:
            self.image = arcade.load_texture(image_path)
        except FileNotFoundError:
            image_path = os.path.expanduser(f"{MY_DIR}/resources/img/missing.jpg")
            self.image = arcade.load_texture(image_path)
        
    def app_module_path():
        # return os.path.expanduser(f"~/{APP_FOLDER}/{selected_app}")
        pass



class GameSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.selected_index = 0

        self.menu_items: list = []

        manifests = get_app_manifests()
        print( manifests )

        for (app_folder_name, manifest_dict) in manifests.items():
            image_path = os.path.expanduser(f"~/{APP_FOLDER}/{app_folder_name}/image.png")

            try:
                game_name = f"{manifest_dict['name']}"

                self.menu_items.append( MenuItem(app_folder_name, game_name, manifest_dict, image_path) )
            except KeyError:
                logger.error(f"KeyError in {app_folder_name} manifest.json")
                continue

        print( self.menu_items )

    
    def on_show_view(self):
        logger.info("Starting GameSelectView")
        arcade.set_background_color(arcade.color.BLACK)

        # self.selected_index = 0


    def on_update(self, delta_time):
        pass


    def on_draw(self):
        width, height = self.window.get_size()
        arcade.start_render()

        x = width * 0.1
        y = height // 2
        for i, item in enumerate(self.menu_items):
            if i == self.selected_index:
                color = arcade.color.YELLOW
            else:
                color = arcade.color.GRAY

            # text = self.menu_items[self.selected_index].name
            text = item.game_name
            arcade.draw_text(text, x, y - i * 20, color, font_size=16, anchor_x="left")

        image = self.menu_items[self.selected_index].image
        image_width = image.width * 0.5
        image_height = image.height * 0.5
        arcade.draw_texture_rectangle(width * 0.8, height * 0.5, image_width, image_height, image, 0)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif symbol == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)

        # QUIT
        elif symbol == arcade.key.ESCAPE:
            self.window.close()

        # elif symbol == arcade.key.TAB:
            # self.window.minimize()

        # LAUNCH APP
        elif symbol == arcade.key.ENTER:
            selected_app = self.menu_items[self.selected_index].module_name
            logger.debug("Launching python module: %s", selected_app)


            # check for sufficient 'coins'
            logger.debug("Checking for sufficient coins")
            if not FREE_PLAY:
                # toast("Excuse me... YOU NEED TO PAY UP!!") #TODO
                logger.error("You don't have enough coins")
                return


            # arcade.set_background_color(arcade.color.WHITE)
            if FULLSCREEN:
                self.window.set_fullscreen(False)
            # self.window.set_visible(False) # doesn't do anything...?
            # self.window.minimize()

            # This is a blocking call - we will wait for the game to run and exit
            args = ["python3", "-m", selected_app]
            cwd = os.path.expanduser(f"~/{APP_FOLDER}")
            logger.debug(f"subprocess.run({args=}, {cwd=})")
            ret_code = subprocess.run(args, cwd=cwd).returncode

            if ret_code != 0:
                logger.error(f"app '{selected_app}' returned non-zero! {ret_code=}")
                self.window.show_view( ErrorModalView("App crashed!", self) )

            # arcade.set_background_color(arcade.color.BLACK)
            # self.window.set_visible(True) # doesn't do anything...?
            # self.window.maximize()
            if FULLSCREEN:
                self.window.set_fullscreen(True)
