import time
import logging

import arcade


from arcade_os.app import app
from arcade_os.config import SPLASH_SCREEN_TIME_DELAY



class SplashScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)



    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        logging.debug(f"load_time: {self.start_time}")



    def on_update(self, delta_time):
        if time.time() > self.start_time + SPLASH_SCREEN_TIME_DELAY:
            from arcade_os.views.MainView import MainView

            if app.get_instance().input_layout:
                next_view = MainView()
            else:
                from arcade_os.views.LearnControllers import LearnControllers
                next_view = LearnControllers( return_view=MainView() )

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

