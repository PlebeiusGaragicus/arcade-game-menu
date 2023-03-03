import arcade
import threading
import logging



from arcade_os.app import FULLSCREEN



class LaunchView(arcade.View):
    def __init__(self, return_view: arcade.View):
        super().__init__()

        self.return_view = return_view



    # def on_draw(self):
    #     arcade.start_render()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)




    def on_update(self, delta_time):
        # check the number of running threads
        # if there are no running threads, then the game has exited
        if threading.active_count() == 1:
            logging.info("game has exited - switching back!")

            # maximize doesn't work... but activate does... shrug emoji here :shrug:
            # arcade.get_window().maximize()
            arcade.get_window().activate()

            if FULLSCREEN:
                arcade.get_window().set_fullscreen(True)

            self.window.show_view( self.return_view)
