import time
# import logging
# logger = logging.getLogger("lnarcade")

import arcade

from lnarcade.app import App

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


class ToastErrorView(arcade.View):
    def __init__(self, toast_message: str, return_view: arcade.View, time_limit: float = 5.0):
        super().__init__()
        self.message = toast_message
        self.start_time = None
        self.return_view = return_view
        self.time_limit = time_limit

    def on_show_view(self):
        self.start_time = time.time()
        # arcade.set_background_color(arcade.color.RED)

        arcade.draw_ellipse_filled( arcade.get_window().width // 2, 50, arcade.get_window().width * 0.8, 60, arcade.color.RED)
        arcade.draw_text(self.message, 10, 15, arcade.color.WHITE, font_size=15, anchor_x="left")

    def on_update(self, delta_time):
        if time.time() > self.start_time + self.time_limit:
            App.get_instance().window.show_view( self.return_view )


    def on_draw(self):
        pass
        # arcade.start_render()

        # arcade.draw_lrtb_rectangle_filled()
        # arcade.draw_ellipse_filled( arcade.get_window().width // 2, 50, arcade.get_window().width * 0.8, 60, arcade.color.RED)

        # arcade.draw_text(self.message, 10, 15, arcade.color.WHITE, font_size=15, anchor_x="left")



class ErrorModalView(arcade.View):
    def __init__(self, toast_message: str, return_view: arcade.View):
        super().__init__()
        self.message = toast_message
        self.start_time = None
        self.return_view = return_view
        self.width, self.height = arcade.get_display_size()

    def on_show_view(self):
        self.start_time = time.time()
        arcade.set_background_color(arcade.color.RED)

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()

        # arcade.draw_ellipse_filled( arcade.get_window().width // 2, 50, arcade.get_window().width * 0.8, 60, arcade.color.RED)
        arcade.draw_text("ERROR", self.width // 2, self.height * 0.8, arcade.color.YELLOW, font_size=30, anchor_x="center")
        arcade.draw_text("PRESS <ENTER> TO CONTINUE", self.width // 2, self.height * 0.1, arcade.color.BLUE, font_size=30, anchor_x="center")
        arcade.draw_text(self.message, 10, self.height // 3, arcade.color.WHITE, font_size=15, anchor_x="left")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            if self.return_view is None:
                arcade.exit()
            else:
                App.get_instance().window.show_view( self.return_view )
