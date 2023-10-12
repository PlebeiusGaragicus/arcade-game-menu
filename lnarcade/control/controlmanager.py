tips = """
https://www.youtube.com/watch?v=Rt5xtIyxgco

https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux

https://learn.adafruit.com/custom-hid-devices-in-circuitpython

https://learn.adafruit.com/adafruit-i2c-qt-rotary-encoder/python-circuitpython

https://learn.adafruit.com/circuitpython-libraries-on-any-computer-with-mcp2221/post-install-checks


"""



import os
import platform
import logging
logger = logging.getLogger()

class ControlManager():
    def __init__(self):
        self.setup_correctly = False

        # check if on MacOS
        if platform.system() == 'Darwin':
            logger.critical("ControlManager::__init__() -> ControlManager not supported on MacOS")
            return

        if os.getenv( "BLINKA_MCP2221", None ) is None:
            logger.critical("ControlManager::__init__() -> BLINKA_MCP2221 not set")
            return
        
        return

        import hid
        device = hid.device()
        device.open(0x04D8, 0x00DD)

        self.setup_correctly = True


    def run(self):
        logger.info("running control manager run()")

        if platform.system() == 'Darwin':
            logger.critical("ControlManager::run() returning -> not supported on MacOS")
            return

        if not self.setup_correctly:
            logger.critical("ControlManager::run() returning -> not setup correctly")
            return

        return

        # this caused the menu screen to go REALLY slow...
        while True:
            pass
