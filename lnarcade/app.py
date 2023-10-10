import os
import threading
import dotenv

import logging
# logger = logging.getLogger("lnarcade")
logger = logging.getLogger()

import arcade

from lnarcade.logger import setup_logging
from lnarcade.config import MY_DIR, DOT_ENV_PATH, create_default_dot_env

GAME_WINDOW: arcade.Window = None

class Singleton:
    _instance = None

    def __init__(self):
        # Singleton pattern must prevent normal instantiation
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance



class App(Singleton):

    # Declare class member vars with type hints to enable richer IDE support throughout the code.
    # buttons: HardwareButtons = None
    # storage: SeedStorage = None
    # settings: Settings = None
    window: arcade.Window = None


    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance:
            return cls._instance
        else:
            # Instantiate the one and only app instance
            return cls.configure_instance()


    @classmethod
    def configure_instance(cls, disable_hardware=False):

        if cls._instance:
            raise Exception("Instance already configured")

        # Instantiate the one and only app instance
        app = cls.__new__(cls)
        cls._instance = app

        # load environment variables
        if dotenv.load_dotenv( DOT_ENV_PATH ) == False:
            # TODO: should I make this a critical error?
            print("WARNING!!!  No .env file found!!!")
            create_default_dot_env()
            # exit(1)
        else:
            with open(DOT_ENV_PATH, 'r') as f:
                print( f.read() )

        print('\n\n\n\n\n###############################################')
        setup_logging()
        logger.debug("Configuring application instance...")

        logging.debug("lnarcade installed at: %s", MY_DIR)

        app.width, app.height = arcade.get_display_size()

        # if FULLSCREEN:
        #     app.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        # else:
        #     app.window = arcade.Window(width=width, height=height, title=SCREEN_TITLE, fullscreen=False, style="borderless")

        app.window = arcade.Window(width=app.width, height=app.height, title="lnarcade", fullscreen=False, style="borderless")


        # TODO: setup threads for hardware buttons
        # controller.microsd = MicroSD.get_instance()
        # controller.microsd.start_detection()

        app.screensaver_activation_ms = 10 * 1000

        # if os.getenv("SCREENSAVER_ENABLED", "1") == "1":
        #     from lnarcade.views.screensaver import ScreensaverView
        #     app.screensaver_view = ScreensaverView()

        if os.getenv("DEBUG", False):
            app.window.set_mouse_visible(False)
        # arcade.run() # THIS IS BLOCKING and has been moved to start()

        return cls._instance


    def start(self):
        logger.debug("App.get_instance().start()")

        global GAME_WINDOW
        GAME_WINDOW = self.window

        from lnarcade.views.splash_screen import SplashScreen
        view = SplashScreen()
        self.window.show_view(view)

        arcade.run()

def main():
    """ This is the entry point for the application when installed via setup.py"""
    App.get_instance().start()
