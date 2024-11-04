import customtkinter as ctk

from view.frame.frame_detalhes_feirante import FrameDetalhesFeirante


class ViewDetalhesFeirante(ctk.CTkFrame):
    def __init__(self, master, controller_main):
        super().__init__(master)
        self.configure(fg_color='white', corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.detalhes = FrameDetalhesFeirante(self, controller_main, controller_main.usuario_logado)
        self.detalhes.grid(row=0, column=0, sticky='nsew')
