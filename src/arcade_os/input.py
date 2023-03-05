from enum import Enum, auto



from pyglet.input import Joystick


MOVEMENT_SPEED = 5
DEAD_ZONE = 0.05




# class InputMapping:
#     """ A mapping of input names to their corresponding input values """
#     def __init__(self):
#         self.mapping = {
#             "up": None,
#             "down": None,
#             "left": None,
#             "right": None,
#             "a": None,
#             "b": None,
#             "x": None,
#             "y": None,
#             "l": None,
#             "r": None,
#             "select": None,
#             "start": None,

#             "rewind": None,
#             "quit": None,
#             "save_state": None,
#             "load_state": None,
#         }




class InputSource:
    # WARNING: THESE ARE CLASS VARIABLES - NOT INSTANCE VARIABLES!
    # joystick: Joystick = None
    # input_mapping: InputMapping = None
    # repeat_lock: bool = False

    def __init__(self, joystick: Joystick):
        self.joystick: Joystick = joystick
        # self.input_mapping: InputMapping = input_mapping
        # self.input_mapping: dict = input_mapping
        self.mapping = None
        self.repeat_lock = False

    @property
    def name(self):
        return self.joystick.device.name
    
    @property
    def id(self):
        return self.joystick.device.manufacturer






class SNESButton():
    """ Enum for SNES controller buttons """
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    L: int = 4
    R: int = 5
    SELECT: int = 6
    START: int = 7
    UP: int = 8
    DOWN: int = 9
    LEFT: int = 10
    RIGHT: int = 11



class N64Button():
    """ Enum for N64 controller buttons """
    A: int = 2
    B: int = 1
    Z: int = 6
    C_UP: int = 9
    C_DOWN: int = 3
    C_LEFT: int = 0
    C_RIGHT: int = 8
    L: int = 4
    R: int = 5
    START: int = 12

    # TODO: THESE AREN'T REGISTERING!!!
    UP: int = 4
    DOWN: int = 5
    LEFT: int = 6
    RIGHT: int = 7



class DragonRiseButton():
    """ Enum for DragonRise controller buttons """
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    L: int = 4
    R: int = 5
    SELECT: int = 6
    START: int = 7
    UP: int = 8
    DOWN: int = 9
    LEFT: int = 10
    RIGHT: int = 11



class InputStyle(Enum):
    KEYBOARD: int = auto()
    SNES: int = auto()
    N64: int = auto()
    DRAGONRISE: int = auto()



# class InputModality:
#     def __init__(self, controller, input_style: InputStyle = InputStyle.KEYBOARD, button_map: dict = None):
#         self.controller = controller
#         self.input_style = input_style
#         self.button_map = button_map

#         self.repeat_lock = False





# class InputMapping(arcade.View):
#     def __init__(self, game_select_view, input_style, controller):
#         super().__init__()
#         self.next_view = GameSelectView



#     def on_show_view(self):
#         arcade.set_background_color(arcade.color.SMOKY_BLACK)



#     def on_draw(self):
#         width, height = self.window.get_size()

#         # arcade.start_render()
#         self.window.clear()
#         arcade.draw_text("Map inputs", width // 2, height * 0.95, arcade.color.YELLOW_ROSE, font_size=24, bold=True, align="center", width=width, anchor_x="center", anchor_y="center")
