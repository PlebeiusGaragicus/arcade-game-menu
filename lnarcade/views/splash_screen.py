import os
import time
import logging
logger = logging.getLogger("lnarcade")

import arcade

from lnarcade.config import MY_DIR

# for type hinting
from pyglet.media import Player

SPLASH_SCREEN_TIME_DELAY = 6.5

class SplashScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.player: Player = None
        self.theme_len = 0

    
    def on_show_view(self):
        logger.info("Starting SplashScreen")
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        logger.debug(f"load_time: {self.start_time}")

        if os.getenv("DEBUG", False):
            sound_path = os.path.join(MY_DIR, 'resources', 'sounds', 'short.wav')
        else:
            sound_path = os.path.join(MY_DIR, 'resources', 'sounds', 'theme.wav')

        theme_sound = arcade.sound.load_sound( sound_path )
        self.theme_len = arcade.sound.Sound.get_length( theme_sound )

        self.player = arcade.sound.play_sound( theme_sound )



    def on_update(self, delta_time):
        # logging.debug(f"delta_time: {delta_time}")

        # if time.time() > self.start_time + SPLASH_SCREEN_TIME_DELAY:
        if time.time() > self.start_time + self.theme_len: # wait for theme to finish
            arcade.sound.stop_sound( self.player )
            # self.show_next_view()

            from lnarcade.views.game_select import GameSelectView
            next_view = GameSelectView()
            self.window.show_view(next_view)


    def on_draw(self):
        width, height = self.window.get_size()

        # self.clear()
        arcade.start_render()

        color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        arcade.draw_text("Loading screen...", width / 2, height / 2,
                         color_with_alpha,
                         font_size=30, anchor_x="center")
        self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
