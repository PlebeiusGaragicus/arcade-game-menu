import arcade
import threading
import logging

from src.utilities.launch import FULLSCREEN

class BlankView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)



    def on_draw(self):
        arcade.start_render()



    def on_update(self, delta_time):

        # if self.game_running:
            # check the number of running threads
            # if there are no running threads, then the game has exited
        if threading.active_count() == 1:
            logging.info("game has exited - switching back!")
            self.game_running = False

            # maximize doesn't work... but activate does... shrug emoji here :shrug:
            # arcade.get_window().maximize()
            arcade.get_window().activate()
            if FULLSCREEN:
                arcade.get_window().set_fullscreen(True)

            from src.views.GameSelectView import GameSelectView
            view = GameSelectView()
            self.window.show_view(view)
