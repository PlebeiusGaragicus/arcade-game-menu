import arcade
import logging

class SettingsView(arcade.View):
    def __init__(self, return_view):
        super().__init__()

        self.return_view = return_view



    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)



    def on_draw(self):
        width, height = self.window.get_size()

        self.clear()
        arcade.draw_text("Settings", width / 2, height / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")



    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)
