import os
import time

from dataclasses import dataclass
import subprocess
import logging
logger = logging.getLogger()

import arcade

from lnarcade.config import APP_FOLDER, MY_DIR
from lnarcade.app import App, GAME_WINDOW
from lnarcade.utilities.find_games import get_app_manifests
from lnarcade.views.error import ErrorModalView



@dataclass
class GameListItem:
    module_name: str
    game_name: str
    manifest_dict: dict
    image_path: str
    image: arcade.Texture = None

    def __post_init__(self):  # This method is automatically called after `__init__`
        try:
            self.image = arcade.load_texture(self.image_path)
        except FileNotFoundError:
            image_path = os.path.expanduser(f"{MY_DIR}/resources/img/missing.jpg")
            self.image = arcade.load_texture(image_path)




class GameSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.selected_index = 0
        self.last_input_time = time.time()
        self.menu_items: list = []
        self.credits: int = 0

        self.mouse_pos = (0, 0)

        manifests = get_app_manifests()
        logger.debug("manifests: %s", manifests)

        for (app_folder_name, manifest_dict) in manifests.items():
            image_path = os.path.expanduser(f"~/{APP_FOLDER}/{app_folder_name}/image.png")

            try:
                game_name = f"{manifest_dict['name']}"

                self.menu_items.append( GameListItem(app_folder_name, game_name, manifest_dict, image_path) )
            except KeyError:
                logger.error(f"KeyError in {app_folder_name} manifest.json")
                continue

        logger.debug("self.menu_items: %s", self.menu_items)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        # TODO - clean this up...
        if self.menu_items == []:
            App.get_instance().window.show_view( ErrorModalView("No manifests found!", None) )

        # self.selected_index = 0


    def on_update(self, delta_time):
        if time.time() - self.last_input_time > int(os.getenv("AFK_SCROLL_TIME", 300)):
            # self.window.show_view( App.get_instance().screensaver_view )
            # simulate keypress
            self.on_key_press(arcade.key.DOWN, 0)


    def on_draw(self):
        arcade.start_render()

        x = GAME_WINDOW.width * 0.1
        y = GAME_WINDOW.height // 2
        for i, menu_item in enumerate(self.menu_items):
            if i == self.selected_index:
                color = arcade.color.YELLOW
                menu_item_size = 40
                arcade.draw_text(">", x - 40, y - i * 50, color, font_size=40, anchor_x="left")
            else:
                menu_item_size = 30
                color = arcade.color.AIR_FORCE_BLUE

            arcade.draw_text(menu_item.game_name, x, y - i * 50, color, font_size=menu_item_size, anchor_x="left")


        # SHOW GAME ARTWORK
        image = self.menu_items[self.selected_index].image
        image_width = image.width * 0.5
        image_height = image.height * 0.5
        arcade.draw_texture_rectangle(GAME_WINDOW.width * 0.8, GAME_WINDOW.height * 0.5, image_width, image_height, image, 0)

        self.flash_free_play()

        # SHOW MOUSE POSITION
        if os.getenv("DEBUG", False):
            self.show_mouse_position()


    def on_key_press(self, symbol: int, modifiers: int):
        self.last_input_time = time.time()

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
            if not os.getenv("FREE_PLAY", False):
                # toast("Excuse me... YOU NEED TO PAY UP!!") #TODO
                logger.error("You don't have enough coins")
                return


            # doesn't do anything...?  Is it because I'm no in a draw loop or something????
            # arcade.set_background_color(arcade.color.BLACK)
            # arcade.start_render()
            
            # DEPRECATED:
            # if FULLSCREEN:
                # self.window.set_fullscreen(False)
            # self.window.set_visible(False) # doesn't do anything...?
            # self.window.minimize()

            args = ["python3", "-m", selected_app]
            cwd = os.path.expanduser(f"~/{APP_FOLDER}")
            logger.debug(f"subprocess.run({args=}, {cwd=})")
            ret_code = subprocess.run(args, cwd=cwd).returncode # This is a blocking call - wait for game to run and exit

            if ret_code != 0:
                logger.error(f"app '{selected_app}' returned non-zero! {ret_code=}")
                self.window.show_view( ErrorModalView("App crashed!", self) )

            # arcade.set_background_color(arcade.color.BLACK)
            # self.window.set_visible(True) # doesn't do anything...?
            # self.window.maximize()

            # DEPRECATED:
            # if FULLSCREEN:
            #     self.window.set_fullscreen(True)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = (x, y)
        # return super().on_mouse_motion(x, y, dx, dy)
    
    def show_mouse_position(self):
        anchor_x = "left"
        offset = 20

        if self.mouse_pos[0] > GAME_WINDOW.width * 0.5:
            anchor_x = "right"
            offset = -20

        if self.mouse_pos[1] > GAME_WINDOW.height * 0.5:
            offset -= offset * 2

        arcade.draw_text(f"{self.mouse_pos}", self.mouse_pos[0], self.mouse_pos[1] + offset, arcade.color.WHITE, font_size=16, anchor_x=anchor_x)
        arcade.draw_text(f"{round(self.mouse_pos[0] / GAME_WINDOW.width * 100, 0)}%  {round(self.mouse_pos[1] / GAME_WINDOW.height * 100, 0)}%", self.mouse_pos[0], self.mouse_pos[1] + offset * 2, arcade.color.GREEN, font_size=16, anchor_x=anchor_x)
        arcade.draw_point(self.mouse_pos[0], self.mouse_pos[1], arcade.color.RED, 5)


    def flash_free_play(self):
        if os.getenv("FREE_PLAY", False):
            # alpha = abs((time.time() % 4) - 1)  # calculate alpha value for fade in/out effect
            alpha = abs((time.time() % 2) - 1)  # calculate alpha value for fade in/out effect
            arcade.draw_text("FREE PLAY", 10, 10, arcade.color.GREEN + (int(alpha * 255),), font_size=26, anchor_x="left")
        else:
            alpha = abs((time.time() % 2) - 1)  # calculate alpha value for fade in/out effect
            arcade.draw_text(f"CREDITS: {self.credits}", 10, 10, arcade.color.RED + (int(alpha * 255),), font_size=26, anchor_x="left")
