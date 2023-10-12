import os
import platform
import logging
logger = logging.getLogger()

class ControlManager():
    def __init__(self):
        # check if on MacOS
        if platform.system() == 'Darwin':
            logger.critical("ControlManager::__init__() -> ControlManager not supported on MacOS")
            return

        # these imports will fail on MacOS
        # import board
        # from rainbowio import colorwheel
        # from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio

        # self.i2c = board.I2C()
        # self.seesaw = seesaw.Seesaw(self.i2c, 0x36)

        # self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        # self.seesaw.pin_mode(24, self.seesaw.INPUT_PULLUP)
        # self.switch = digitalio.DigitalIO(self.seesaw, 24)

        # self.pixel = neopixel.NeoPixel(self.seesaw, 6, 1)
        # self.pixel.brightness = 0.5

        # self.last_position = -1
        # self.color = 0

        # # Get current volume from the system
        # self.volume_query = os.popen("amixer get 'Master' | grep -m1 -o [0-9]*% | tr -d %").read().strip()
        # self.current_volume = int(self.volume_query)

    def run(self):
        logger.info("running control manager run()")
        return

        if platform.system() == 'Darwin':
            logger.critical("ControlManager::run() returning -> not supported on MacOS")
            return

        while True:
            self.position = -self.encoder.position

            if self.position != self.last_position:
                print(self.position)

                if self.switch.value:
                    # Change the LED color.
                    if self.position > self.last_position:
                        self.color += 1
                    else:
                        self.color -= 1
                    self.color = (self.color + 256) % 256
                    self.pixel.fill(self.colorwheel(self.color))
                else:  
                    # Change the system volume.
                    if self.position > self.last_position:
                        self.current_volume = min(100, self.current_volume + 5)  # increase by 5%
                    else:
                        self.current_volume = max(0, self.current_volume - 5)  # decrease by 5%
                    
                    # Adjust system volume using the 'amixer' command
                    v = f"amixer set 'Master' -- {self.current_volume}%"
                    print(v)
                    print(os.system( v ))

            self.last_position = self.position
