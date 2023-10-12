import pywebio

class ArcadeServerPage():
    def __init__(self):
        self.password = "notinthesauce"

    def page(self):
        pywebio.output.put_text("Server page")
        pywebio.output.put_text("Port: %d" % self.server.port)
        pywebio.output.put_text("Password: %s" % self.server.password)

    def start_server(self):
        pywebio.start_server(self.settings, port=8080, auto_open_webbrowser=False)


    def settings(self):
        port = pywebio.input.input("Enter port number", type=pywebio.input.NUMBER)
        password = pywebio.input.input("Enter password", type=pywebio.input.PASSWORD)
        pywebio.output.put_text("Port number: %d" % port)
        pywebio.output.put_text("Password: %s" % password)
