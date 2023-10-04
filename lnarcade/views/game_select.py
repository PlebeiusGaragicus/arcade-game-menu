import time
import logging
logger = logging.getLogger("lnarcade")

import arcade


class GameSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)


    
    def on_show_view(self):
        logger.info("Starting GameSelectView")
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        logger.debug(f"load_time: {self.start_time}")



    def on_update(self, delta_time):
        # logging.debug(f"delta_time: {delta_time}")
        pass



    def on_draw(self):
        width, height = self.window.get_size()

        # self.clear()
        arcade.start_render()

        color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("GAME SELECT", width / 2, height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
