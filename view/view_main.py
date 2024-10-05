import customtkinter as ctk
from view.view_login_cadastro import ViewLoginCadastro

class ViewMain(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.geometry('1280x760')
        self.title('Tem Feira?')
        self.configure(fg_color='white')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = ViewLoginCadastro(self)
        self.frame.grid(sticky='nsew')
