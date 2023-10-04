# import logging
# logger = logging.getLogger("lnarcade")

import arcade

def show_error(error_msg: str):
    window = arcade.get_window()
    window.show_view(ErrorView(error_msg))

    # while True:
    #     pass
    arcade.run() # this is a blocking call... execution should STOP... the arcade is fucked and should completely stop (but not quick as it will be restared by systemd service daemon)

class ErrorView(arcade.View):
    def __init__(self, error_msg: str):
        super().__init__()
        self.error_msg = error_msg

    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)

    def on_update(self, delta_time):
        pass



    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(self.error_msg, 10, 15, arcade.color.WHITE, font_size=15, anchor_x="left")
