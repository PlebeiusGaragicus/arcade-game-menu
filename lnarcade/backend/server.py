tips = """
https://pywebio.readthedocs.io/en/latest/cookbook.html

https://github.com/pywebio/PyWebIO

https://pywebio.readthedocs.io/en/latest/guide.html?highlight=example#layout
"""



import pywebio

class ArcadeServerPage():
    def __init__(self):
        self.password = "asdf"

    def start_server(self):
        pywebio.start_server(applications=self.check_password,
                             host="10.1.10.49",
                             port=8080,
                             auto_open_webbrowser=False,
                            #  remote_access=True
                             )

    def restart(self, action):
        print(action)
        print("RESTART!!")

    def backend_page(self):
        pywebio.output.put_markdown("# Lightning Arcade Settings Backend")
        pywebio.output.put_markdown(tips)
        pywebio.output.put_markdown("---")

        # system command button
        pywebio.output.put_buttons(["restart", "FUCKFUCK"], onclick=self.restart)

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
