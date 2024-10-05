import customtkinter as ctk
from view.view_login_cadastro import ViewLoginCadastro
from view.view_base import ViewBase


class ViewMain(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.geometry('1280x760')
        self.title('Tem Feira?')
        self.configure(fg_color='white')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.map_telas = {
            'login_cadastro': ViewLoginCadastro,
            'base': ViewBase,
        }

        self.frame = ViewBase(self)
        self.frame.grid(sticky='nsew')

    def alternar_telas(self, tela: str):
        self.frame.grid_forget()
        if self.map_telas[tela]:
            self.frame = self.map_telas[tela](self)
            self.frame.grid(sticky='nsew')
