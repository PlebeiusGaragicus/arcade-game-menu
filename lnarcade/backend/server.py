tips = """
https://pywebio.readthedocs.io/en/latest/cookbook.html

https://github.com/pywebio/PyWebIO

https://pywebio.readthedocs.io/en/latest/guide.html?highlight=example#layout
"""

import logging
logger = logging.getLogger()

import pywebio

BUTTON_RESTART = "Kill menu system"
BUTTON_KILL = "Kill currently running app"


from lnarcade.app import App

class ArcadeServerPage():
    def __init__(self):
        self.password = "asdf"

    def start_server(self):
        pywebio.start_server(applications=self.check_password,
                            #  host="10.1.10.49",
                             host="0.0.0.0",
                             port=8080,
                             auto_open_webbrowser=False,
                            )

    def command(self, action):
        if action == BUTTON_RESTART:
            logger.warning("Killing the menu system!")
            App.get_instance().window.close()
            exit(0)

        if action == BUTTON_KILL:
            if App.get_instance().process is None:
                logger.warning("No process to kill")
                pywebio.output.toast("No process to kill", duration=7, color="warn")
                return

            logger.warning("Killing the current process!")
            App.get_instance().kill_running_process()


    def backend_page(self):
        pywebio.output.put_markdown("# Lightning Arcade Settings Backend")
        pywebio.output.put_markdown(tips)
        pywebio.output.put_markdown("---")

        # system command button
        pywebio.output.put_buttons([BUTTON_RESTART, BUTTON_KILL], onclick=self.command)

        # config file
        pywebio.pin.put_input(name="port", type=pywebio.input.NUMBER, value=0)

        pywebio.session.hold()
    
    def check_password(self):
        password = pywebio.input.input("Enter password", type=pywebio.input.PASSWORD)
        if password != self.password:
            return

        self.backend_page()


if __name__ == "__main__":
    server = ArcadeServerPage()
    server.start_server()
