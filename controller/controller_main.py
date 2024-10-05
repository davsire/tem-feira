from view.view_main import ViewMain


class ControllerMain:
    __instancia = None

    def __init__(self):
        self.app = ViewMain()

    def __new__(cls):
        if ControllerMain.__instancia is None:
            ControllerMain.__instancia = object.__new__(cls)
        return ControllerMain.__instancia

    def iniciar_app(self):
        self.app.mainloop()
