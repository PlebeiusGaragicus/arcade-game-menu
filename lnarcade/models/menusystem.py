import logging
logger = logging.getLogger("lnarcade")

import arcade

from lnarcade.models.singleton import Singleton
from lnarcade.config import FULLSCREEN, SCREEN_TITLE


class MenuSystem(Singleton):

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
    def configure_instance(cls, disable_hardware=False):
        logger.info("Configuring MenuSystem")

        if cls._instance:
            raise Exception("Instance already configured")

        # Instantiate the one and only Controller instance
        controller = cls.__new__(cls)
        cls._instance = controller


        width, height = arcade.get_display_size()

        width //= 2
        height //= 2

        if FULLSCREEN:
            controller.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        else:
            controller.window = arcade.Window(width=width, height=height, title=SCREEN_TITLE)

        # controller.storage = SeedStorage()
        # controller.settings = Settings.get_instance()
        # controller.microsd = MicroSD.get_instance()
        # controller.microsd.start_detection()

        controller.screensaver_activation_ms = 10 * 1000
        controller.window.set_mouse_visible(False)
        # arcade.run() # THIS IS BLOCKING and has been moved to start()

        return cls._instance


    def start(self):
        logger.info("MenuSystem::start()")

        from lnarcade.views.splash_screen import SplashScreen
        view = SplashScreen()
        self.window.show_view(view)

        arcade.run()
