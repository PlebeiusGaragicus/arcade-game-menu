import os
import sys
import logging



import arcade



from arcade_os.config import FULLSCREEN, SCREEN_TITLE, SHOW_MOUSE



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
    


######################################################################
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
        the_instance = cls.__new__(cls)
        cls._instance = the_instance

        #####################################################################
        # Initialize the controller with all the cool stuff that WE need/want

        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[logging.StreamHandler()],
            format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s")

        logging.getLogger("arcade").setLevel(logging.WARNING)
        logging.getLogger("PIL").setLevel(logging.INFO)

        the_instance.width, the_instance.height = arcade.get_display_size()

        if FULLSCREEN:
            the_instance.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        else:
            the_instance.window = arcade.Window(width=the_instance.width, height=the_instance.height, title=SCREEN_TITLE)

        if len(sys.argv) == 1:
            home_folder = os.path.expanduser("~")
            the_instance.game_folder = os.path.join(home_folder, "GAMES")

            logging.warning(f"No game folder given - defaulting to {the_instance.game_folder}")
            # sys.exit(1)
        else:
            logging.debug(f"using supplied game folder: {sys.argv[1]}")
            the_instance.game_folder = sys.argv[1]


        # controller.storage = SeedStorage()
        # controller.settings = Settings.get_instance()
        # controller.microsd = MicroSD.get_instance()
        # controller.microsd.start_detection()
        # controller.screensaver_activation_ms = 10 * 1000

        # this can't be here... because this is a blocking function
        # arcade.run()
    
        return cls._instance



    def start(self):

        self.window.set_mouse_visible(False)

        from arcade_os.views.SplashScreen import SplashScreen
        self.window.show_view( SplashScreen() )

        arcade.run()

        ### NOTE:
        ###     arcade.run() is a blocking function
        ###     but start() is the function that gets everything started...
        ###     but by this time everything should be up and running... with control inputs and everything that we'll need...
        ###      for the GameSelectView to 
