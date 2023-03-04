import os
import sys
import platform
import subprocess
import logging

import arcade



from arcade_os.config import FULLSCREEN, SCREEN_TITLE, SNES9X_EMULATOR_PATH, GameTypes



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

    game_list: list = None



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
        singleton = cls.__new__(cls)
        cls._instance = singleton



        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[logging.StreamHandler()],
            format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s")

        logging.getLogger("arcade").setLevel(logging.WARNING)
        logging.getLogger("PIL").setLevel(logging.INFO)

        # controller.storage = SeedStorage()
        # controller.settings = Settings.get_instance()
        # controller.microsd = MicroSD.get_instance()
        # controller.microsd.start_detection()
        # controller.screensaver_activation_ms = 10 * 1000

        singleton.width, singleton.height = arcade.get_display_size()

        if FULLSCREEN:
            singleton.window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
        else:
            singleton.window = arcade.Window(width=singleton.width, height=singleton.height, title=SCREEN_TITLE)

        if len(sys.argv) == 1:
            home_folder = os.path.expanduser("~")
            singleton.game_folder = os.path.join(home_folder, "GAMES")

            logging.warning(f"No game folder given - defaulting to {singleton.game_folder}")
            # sys.exit(1)
        else:
            logging.debug(f"using supplied game folder: {sys.argv[1]}")
            singleton.game_folder = sys.argv[1]

        # singleton.game_list = singleton.search_for_games()
        singleton.search_for_games()


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



    def launch_game(self, game_index: int):
            """
                To launch a game we pass the index of the game in the game_list
            """
            # NOTE: we can't do this here, we need to do it in the main thread
            # arcade.get_window().minimize()
            logging.debug("launch_game()")
            logging.debug(f"{platform.system()=}")

            game = self.game_list[game_index]

            if game['type'] == GameTypes.PYTHON:
                cmd = os.path.join(self.game_folder, self.game_list[game_index]['name'], "run")
            elif game['type'] == GameTypes.SNES:
                cmd = os.path.join(self.game_folder, self.game_list[game_index]['name'], ".zip")
                cmd = SNES9X_EMULATOR_PATH + " \"" + cmd + "\""
                # I CAN ONLY TEST THIS ON A DEBIAN MACHINE WITH SNES9X INSTALLED
                return


            # # if we are running MacOS, return
            # if platform.system() == "Darwin":
            #     logging.warning("MacOS is not supported yet. Sorry :(")
            #     return

            logging.debug(f"{cmd=}")
            process = subprocess.Popen(args="", executable=cmd , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, error = process.communicate()
            logging.debug(f"{output=}")
            logging.debug(f"{error=}")



    def search_for_games(self):
        self.game_list = []

        for file_name in os.listdir( self.game_folder ):
            logging.debug(f"{file_name=}")

            if not os.path.isdir(os.path.join(self.game_folder, file_name)):
                logging.debug("skipping non-directory %s", file_name)
                continue

            # if there is a folder named 'src' inside this directory
            if os.path.isdir(os.path.join(self.game_folder, file_name, "src")):
                type = GameTypes.PYTHON
            else:  # else, if there is a .zip file inside this directory
                type = GameTypes.SNES

            try:
                image_path = os.path.join(self.game_folder, file_name, "image.jpg")
                image = arcade.load_texture( image_path )
            except FileNotFoundError:
                image = arcade.load_texture("assets/missing.jpg")
                logging.error("missing image.jpg")

            self.game_list.append({
                    "name": file_name,
                    # "path": os.path.join(game_folder, file_name),
                    "image": image,
                    "type": type}
                )

            logging.debug(f"found a game: {file_name} at '{os.path.join(self.game_folder, file_name)}' of type {type}")

        logging.debug(self.game_list)
