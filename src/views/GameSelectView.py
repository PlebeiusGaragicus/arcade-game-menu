import logging
import threading

import arcade

from src.config import SHOW_MOUSE
from src.helpers import launch_game
from src.input import SNESButton, N64Button
from src.views.BlankView import BlankView
from src.GameFinder import GameFinder



class GameSelectView(arcade.View):
    def __init__(self):
        super().__init__()

        self.joystick_locks = {}
        joysticks = arcade.get_game_controllers()
        if joysticks:
            self.joystick = []
            for j in joysticks:
                # logging.debug(f"Joystick name: {self.joystick.device.name}")
                logging.debug(f"Joystick name: {j.device.name}")

                self.joystick_locks[j] = False
                self.joystick.append(j)
                j.open()
                # self.joystick.open()


        else:
            logging.warning("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None
        
        # self.joystick_lock = False

        self.game_list = GameFinder.find_games()
        self.selected = 0
        self.move_selection(0) # we need to call this to load the image

        self.mx = 0
        self.my = 0
        self.mouse_cursor = arcade.load_texture("./assets/fire.png")



    def on_show_view(self):
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        if self.joystick:
            for j in self.joystick:
                j.push_handlers(self)
                # self.joystick.push_handlers(self)



    def launch_game(self):
        arcade.get_window().set_fullscreen(False)
        arcade.get_window().minimize()

        if self.joystick:
            for j in self.joystick:
                j.pop_handlers()
                # self.joystick.pop_handlers()

        # create a thread that checks if the launched game is still running
        t = threading.Thread(target=lambda: launch_game( self.game_list[self.selected] ))
        t.start()

        view = BlankView()
        self.window.show_view(view)



    def on_draw(self):
        width, height = self.window.get_size()

        # arcade.start_render()
        self.window.clear()
        # arcade.draw_text("Game Select", width // 2, height * 0.95, arcade.color.YELLOW_ROSE, font_size=24, bold=True, align="center", width=width, anchor_x="center", anchor_y="center")

        # display the image.jpg in the selected game folder
        arcade.draw_texture_rectangle(width//2, height//2, width, height, self.image)

        # for i, game in enumerate(self.game_list):
        #     if i == self.selected:
        #         arcade.draw_text(game['name'], 10, 100 + i * 20, arcade.color.WHITE, 14)
        #     else:
        #         arcade.draw_text(game['name'], 10, 100 + i * 20, arcade.color.GRAY, 14)

        if SHOW_MOUSE:
            arcade.draw_texture_rectangle(self.mx, self.my, 50, 50, self.mouse_cursor)



    def move_selection(self, delta):
        self.selected += delta
        if self.selected < 0:
            self.selected = len(self.game_list) - 1
        elif self.selected >= len(self.game_list):
            self.selected = 0

        try:
            self.image = arcade.load_texture(self.game_list[self.selected]['path'] + "/image.jpg")
        except FileNotFoundError:
            self.image = arcade.load_texture("assets/missing.jpg")
            logging.error("missing image.jpg")







    def on_joyaxis_motion(self, joystick, axis, value):
        # logging.debug(f"Joystick {joystick} axis {axis} moved to {value}")

        # joystick_lock = self.joystick_locks[joystick]

        # if axis == 'y':
        #     if value < 0.5 and value > -0.5:
        #         self.joystick_locks[joystick] = False

        #     if self.joystick_locks[joystick]:
        #         return

        #     if value < -0.5:
        #         logging.debug("JOYSTICK UP")
        #         self.joystick_locks[joystick] = True
        #         self.move_selection(-1)
        #     elif value > 0.5:
        #         logging.debug("JOYSTICK DOWN")
        #         self.joystick_locks[joystick] = True
        #         self.move_selection(1)
        
        if axis == 'x':
            if value < 0.5 and value > -0.5:
                self.joystick_locks[joystick] = False

            if self.joystick_locks[joystick]:
                return

            if value < -0.5:
                logging.debug("JOYSTICK LEFT")
                self.joystick_locks[joystick] = True
                self.move_selection(1)
            elif value > 0.5:
                logging.debug("JOYSTICK RIGHT")
                self.joystick_locks[joystick] = True
                self.move_selection(-1)



    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        # logging.debug(f"Joystick {joystick.device} hat moved to ({hat_x}, {hat_y})")

        if hat_y == 0 and hat_x == 0:
            self.joystick_locks[joystick] = False

        if self.joystick_locks[joystick]:
                return

        # TODO: I need to ensure that additional up/down aren't registered if user presses a sideways key
        # if hat_y == 1:
        #     logging.debug("HAT UP")
        #     self.joystick_locks[joystick] = True
        #     self.move_selection(-1)
        # elif hat_y == -1:
        #     logging.debug("HAT DOWN")
        #     self.joystick_locks[joystick] = True
        #     self.move_selection(1)

        if hat_x == 1:
            logging.debug("HAT RIGHT")
            self.joystick_locks[joystick] = True
            self.move_selection(-1)
        elif hat_x == -1:
            logging.debug("HAT LEFT")
            self.joystick_locks[joystick] = True
            self.move_selection(1)



    def on_joybutton_press(self, _joystick, button):
        if _joystick.device.name == "Joystick name: USB,2-axis 8-button gamepad":
            self.on_snes_button_press(button)
        elif _joystick.device.name == "Pro Controller":
            self.on_pro_controller_button_press(button)
        elif "DragonRise Inc." in _joystick.device.name:
            self.on_dragonrise_button_press(button)

        # if self.joystick.device.name == "Joystick name: USB,2-axis 8-button gamepad":
        #     self.on_snes_button_press(button)
        # elif self.joystick.device.name == "Pro Controller":
        #     self.on_pro_controller_button_press(button)
        # elif "DragonRise Inc." in self.joystick.device.name:
        #     self.on_dragonrise_button_press(button)


    def on_dragonrise_button_press(self, button):
        logging.debug("Button {} down".format(button))



    def on_pro_controller_button_press(self, button):
        logging.debug("Button {} down".format(button))

        if button == N64Button.A:
            logging.debug("A")
            self.launch_game()

        if button == N64Button.START:
            logging.debug("START")
            self.launch_game()



    def on_snes_button_press(self, button):
        logging.debug("Button {} down".format(button))

        if button == SNESButton.A:
            logging.debug("A")
            self.launch_game()

        if button == SNESButton.START:
            logging.debug("START")
            self.launch_game()

        if button == SNESButton.UP:
            logging.debug("UP")
            self.move_selection(1)

        if button == SNESButton.DOWN:
            logging.debug("DOWN")
            self.move_selection(-1)

        if button == SNESButton.LEFT:
            self.move_selection(1)
            logging.debug("LEFT")

        if button == SNESButton.RIGHT:
            self.move_selection(-1)
            logging.debug("RIGHT")



    def on_key_press(self, key, modifiers):
        logging.debug(f"{key=} {modifiers=}")

        if key == arcade.key.UP:
            self.move_selection(1)
        
        if key == arcade.key.DOWN:
            self.move_selection(-1)
        
        if key == arcade.key.LEFT:
            self.move_selection(1)

        if key == arcade.key.RIGHT:
            self.move_selection(-1)

        if key in [arcade.key.ENTER, arcade.key.SPACE]:
            self.launch_game()

        if key in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.close_window()



    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.mx = x
        self.my = y
