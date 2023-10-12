import os
import threading
import subprocess
import dotenv

import logging
logger = logging.getLogger()

import arcade

from lnarcade.logger import setup_logging
from lnarcade.config import MY_DIR, DOT_ENV_PATH, create_default_dot_env
# from lnarcade.control.controlmanager import ControlManager
# from lnarcade.backend.server import ArcadeServerPage

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
    process: subprocess.Popen = None


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

        print('\n\n\n\n\n###############################################')
        
        # load environment variables
        if dotenv.load_dotenv( DOT_ENV_PATH ) == False:
            # TODO: should I make this a critical error?
            print("WARNING!!!  No .env file found at {}".format(DOT_ENV_PATH))
            create_default_dot_env()
        else:
            with open(DOT_ENV_PATH, 'r') as f:
                print("DOT_ENV_PATH: %s", DOT_ENV_PATH)
                print( f.read() )

        setup_logging()
        logger.debug("Configuring application instance...")

        logging.debug("lnarcade installed at: %s", MY_DIR)

        app.width, app.height = arcade.get_display_size()

        # if FULLSCREEN:
        #     app.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        # else:
        #     app.window = arcade.Window(width=width, height=height, title=SCREEN_TITLE, fullscreen=False, style="borderless")

        app.window = arcade.Window(width=app.width, height=app.height, title="lnarcade", fullscreen=False, style="borderless")
        app.window.set_mouse_visible(False)

        from lnarcade.control.controlmanager import ControlManager
        from lnarcade.backend.server import ArcadeServerPage
        app.controlmanager = ControlManager()
        app.backend = ArcadeServerPage()


        return cls._instance


    def start(self):
        logger.debug("App.get_instance().start()")

        global GAME_WINDOW
        GAME_WINDOW = self.window

        # start seperate thread to run control manager
        control_thread = threading.Thread(target=self.controlmanager.run)
        control_thread.daemon = True # this is needed so that when the main process exits the control thread will also exit
        control_thread.start()

        backend_thread = threading.Thread(target=self.backend.start_server)
        backend_thread.daemon = True
        backend_thread.start()

        from lnarcade.views.splash_screen import SplashScreen
        view = SplashScreen()
        self.window.show_view(view)

        try:
            arcade.run()
        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt")
            arcade.Window.close(self.window)
            control_thread.join(0.0)
            backend_thread.join(0.0)

        logger.debug("App.get_instance().start() - END")
        exit(0)

    def kill_running_process(self):
        if self.process is None:
            logger.warning("No process to kill")
            return

        self.process.terminate()
        self.process = None
