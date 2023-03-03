import logging
import threading

import arcade

from control.input import SNESButton, N64Button, DragonRiseButton
from src.views.GameSelectView import GameSelectView



class InputMapping(arcade.View):
    def __init__(self, game_select_view, input_style, controller):
        super().__init__()
        self.next_view = GameSelectView



    def on_show_view(self):
        arcade.set_background_color(arcade.color.SMOKY_BLACK)



    def on_draw(self):
        width, height = self.window.get_size()

        # arcade.start_render()
        self.window.clear()
        arcade.draw_text("Map inputs", width // 2, height * 0.95, arcade.color.YELLOW_ROSE, font_size=24, bold=True, align="center", width=width, anchor_x="center", anchor_y="center")
