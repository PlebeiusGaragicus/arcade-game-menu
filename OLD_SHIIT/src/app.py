import logging

import arcade


from src.utilities.launch import SCREEN_TITLE, FULLSCREEN
from src.models import Singleton


FULLSCREEN = True
SHOW_MOUSE = False
SCREEN_TITLE = "Starting Template"
SPLASH_SCREEN_TIME_DELAY = 0.5
SNES9X_EMULATOR_PATH = "flatpak run com.snes9x.Snes9x"



class app(Singleton):
    VERSION = "0.0.3"

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
            # Instantiate the one and only Controller instance
            return cls.configure_instance()



    @classmethod
    def configure_instance(cls):
        if cls._instance:
            raise Exception("Instance already configured")

        # Instantiate the one and only Controller instance
        controller = cls.__new__(cls)
        cls._instance = controller


        #####################################################################
        # Initialize the controller with all the cool stuff that WE need/want

        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[logging.StreamHandler()],
            format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s")

        logging.getLogger("arcade").setLevel(logging.WARNING)
        logging.getLogger("PIL").setLevel(logging.INFO)

        width, height = arcade.get_display_size()

        if FULLSCREEN:
            window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        else:
            window = arcade.Window(width=width, height=height, title=SCREEN_TITLE)

        window.set_mouse_visible(False)
        arcade.run()


        # controller.storage = SeedStorage()
        # controller.settings = Settings.get_instance()
        # controller.microsd = MicroSD.get_instance()
        # controller.microsd.start_detection()
        # controller.screensaver_activation_ms = 10 * 1000
    
        return cls._instance



    def start(self):
        from src.views.SplashScreen import SplashScreen
        view = SplashScreen()
        self.window.show_view(view)
