import arcade
import logging
from typing import List

from pyglet.input import Joystick



class LearnControllers(arcade.View):
    def __init__(self, return_view: arcade.View):
        super().__init__()

        self.return_view = return_view

        self.joystick: List[Joystick] = None



    def on_show_view(self):
        arcade.set_background_color(arcade.color.RICH_BLACK)

        # self.setup_controllers()

    
    def setup_controllers(self):
        joysticks = arcade.get_game_controllers()

        if joysticks:
            self.joystick = []
            for j in joysticks:
                # logging.debug(f"Joystick name: {self.joystick.device.name}")
                logging.debug(f"Joystick name: {j.device.name}")

                self.joystick_locks[j] = False
                self.joystick.append(j)
                j.open()
        else:
            logging.warning("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None



    def on_draw(self):
        arcade.start_render()



    def on_update(self, delta_time):
        if False:
            self.window.show_view( self.return_view )
