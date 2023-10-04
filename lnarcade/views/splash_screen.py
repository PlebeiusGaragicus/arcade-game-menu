import time
import logging
logger = logging.getLogger("lnarcade")

import arcade

SPLASH_SCREEN_TIME_DELAY = 5

class SplashScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)


    
    def on_show_view(self):
        logger.info("Starting SplashScreen")
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        logger.debug(f"load_time: {self.start_time}")



    def on_update(self, delta_time):
        # logging.debug(f"delta_time: {delta_time}")

        if time.time() > self.start_time + SPLASH_SCREEN_TIME_DELAY:
            self.show_next_view()



    def on_draw(self):
        width, height = self.window.get_size()

        # self.clear()
        arcade.start_render()

        color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("Loading screen...", width / 2, height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255



    def show_next_view(self):
        # from src.views.adventure_view import AdventureView
        from lnarcade.views.game_select import GameSelectView
        # create and show the next view (in this case, a new instance of MyGame)
        # next_view = AdventureView()
        next_view = GameSelectView()
        # next_view.setup()
        self.window.show_view(next_view)
