import os
import time
import logging
logger = logging.getLogger("lnarcade")

import arcade

from lnarcade.config import APP_FOLDER
from lnarcade.utilities.find_games import get_app_manifests


class GameSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.manifests: dict = None
        self.selected_index = 0

    
    def on_show_view(self):
        logger.info("Starting GameSelectView")
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        logger.debug(f"load_time: {self.start_time}")

        self.manifests = get_app_manifests()

        print( self.manifests )


    def on_update(self, delta_time):
        pass


    def on_draw(self):
        width, height = self.window.get_size()
        arcade.start_render()

        # Draw the list of manifests
        x = width * 0.1
        y = height // 2
        for i, (name, data) in enumerate(self.manifests.items()):
            if i == self.selected_index:
                color = arcade.color.YELLOW
                image_path = os.path.expanduser(f"~/{APP_FOLDER}/{name}/image.png")
            else:
                color = arcade.color.GRAY

            text = f"{data['name']} - {data['data']}"
            arcade.draw_text(text, x, y - i * 20, color, font_size=16, anchor_x="left")

        # Load and draw the image
        image = arcade.load_texture(image_path)
        image_width = image.width * 0.5
        image_height = image.height * 0.5
        arcade.draw_texture_rectangle(width * 0.8, height * 0.5, image_width, image_height, image, 0)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.manifests)
        elif symbol == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.manifests)
