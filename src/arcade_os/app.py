import os
import sys
import platform
import subprocess
import logging
from typing import List

# TODO: am I doing this wrong?
import json
from json import JSONDecodeError


import arcade


from arcade_os.input import InputSource
from arcade_os.config import FULLSCREEN, SCREEN_TITLE, SNES9X_EMULATOR_PATH, GameTypes, CONTROLLER_JSON_FILENAME



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
    input_sources: List[InputSource] = None



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
        singleton.game_list = singleton.search_for_games()

        singleton.input_sources = singleton.setup_controllers()


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
        ret_list = []

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

            ret_list.append({
                    "name": file_name,
                    # "path": os.path.join(game_folder, file_name),
                    "image": image,
                    "type": type}
                )

            logging.debug(f"found a game: {file_name} at '{os.path.join(self.game_folder, file_name)}' of type {type}")

        logging.debug(ret_list)
        return ret_list


    # def setup_controllers(self):
    #     """
    #         TODO: This doesn't need to be a member function of the Controller class
    #         This will return None on error, or if the file doesn't exist
    #     """

    #     input_sources = []
    #     # REMEMBER: calling this function will nullify any previously saved/setup controllers.  In order for persistance... we can't call this function unless we are wiping away the old setup
    #     controllers = arcade.get_game_controllers()

    #     if not controllers:
    #         logging.error("No controllers found")
    #         return None

    #     for c in controllers:
    #         logging.debug(f"{c=}")

    #         # new input source with the given joystick object, as well as a blank input mapping
    #         new_source = InputSource(c, InputMapping())

    #         # we must do this!
    #         c.open()

    #         input_sources.append( new_source )
    #         logging.debug(f"{input_sources=}")

    #     try: # to open the input layout file...
    #         input_layout_file = os.path.join(self.game_folder, CONTROLLER_JSON_FILENAME)
    #         with open(input_layout_file, 'rb') as f:
    #             input_file_contents = json.load(f)
    #             logging.debug(f"{input_file_contents=}")
    #     except FileNotFoundError:
    #         logging.error("No input layout file found")
    #         input_file_contents = None

    #     try:
    #         for c, i in enumerate( input_file_contents['controllers'] ):
    #             c[i].mapping = c['mapping']

    #             for key, value in c['mapping'].items():
    #                 print(f"{key}: {value}")
    #             print()

    #     except JSONDecodeError:
    #         logging.error("Error parsing input layout file")
    #         return None

    #     logging.debug(f"{input_sources=}")

    #     if input_sources == []:
    #         logging.error("No controllers found")
    #         return None

    #     return input_sources


    def setup_controllers(self):
        """
        TODO: This doesn't need to be a member function of the Controller class
        This will return None on error, or if the file doesn't exist
        """

        input_sources = []
        # REMEMBER: calling this function will nullify any previously saved/setup controllers.  In order for persistance... we can't call this function unless we are wiping away the old setup
        controllers = arcade.get_game_controllers()

        for c in controllers:
            print("FOUND:")
            print(c.device.name)
            c.open()

        if not controllers:
            logging.error("No controllers found")
            return None

        # for c in controllers:
        #     logging.debug(f"setting up controller: {c.device.name=}")

        #     # new input source with the given joystick object, as well as a blank input mapping
        #     # new_source = InputSource(c, InputMapping())
        #     new_source = InputSource(c)

        #     # we must do this!
        #     c.open()

        #     input_sources.append(new_source)
        #     logging.debug(f"{input_sources=}")

        try: # to open the input layout file...
            input_layout_file = os.path.join(self.game_folder, CONTROLLER_JSON_FILENAME)
            with open(input_layout_file, 'r') as f:
                input_file_contents = json.load(f)
                logging.debug(f"{input_file_contents=}")
        except FileNotFoundError:
            logging.error("No input layout file found")
            input_file_contents = None
        
        if input_file_contents is None:
            return None


        for controller in input_file_contents['controllers']:
            # Get the name of the controller from the input layout file
            controller_name = controller['name']
            # Get the mapping dictionary for the controller from the input layout file
            mapping = controller['mapping']

            # Find the input source that matches the controller by name
            for c in controllers:
                print("EQUAL?")
                print( f"'{c.device.name}' '{controller_name}'")
                if c.device.name == controller_name:
                    # Set the input mapping for the input source
                    # input_source.mapping = mapping
                    logging.debug(f"setting up controller: {c.device.name=}")

                    # new input source with the given joystick object, as well as a blank input mapping
                    # new_source = InputSource(c, InputMapping())
                    new_source = InputSource(c)
                    new_source.mapping = mapping

                    # we must do this!
                    # c.open()

                    input_sources.append(new_source)

        logging.debug(f"{input_sources=}")

        if input_sources == []:
            logging.error("No controllers found")
            return None

        return input_sources


