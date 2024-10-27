import customtkinter as ctk
from tkintermapview import TkinterMapView

class ViewMapa(ctk.CTkFrame):
    
    def __init__(self, master, controller_main):
        super().__init__(master)
        self.__controller_main = controller_main
        
        self.configure(fg_color='white', corner_radius=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        
        self.mapa = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.mapa.grid(row=0, column=0, sticky='nsew')

        latitude, longitude = self.__controller_main.obter_localizacao_usuario_logado()
        self.mapa.set_position(latitude, longitude)
        self.mapa.set_zoom(12)

        self.plotar_feiras()
        self.plotar_usuario_logado()
        self.criar_legenda()

    def plotar_feiras(self):
        localizacoes = self.__controller_main.obter_localizacoes_feirantes()
        for nome_feira, latitude, longitude in localizacoes:
            self.mapa.set_marker(latitude, longitude, text=nome_feira, marker_color_circle='red', marker_color_outside='#bf1900')
        
    def plotar_usuario_logado(self):
        localizacao_usuario = self.__controller_main.obter_localizacao_usuario_logado()
        if localizacao_usuario:
            latitude, longitude = localizacao_usuario
            self.mapa.set_marker(latitude, longitude, text="Sua casa", marker_color_circle='#90EE90', marker_color_outside='#00bf63')

    def criar_legenda(self):
        legenda_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=0)
        legenda_frame.grid(row=2, column=0, sticky='ew', pady=10)

        casa_legenda = ctk.CTkLabel(
            legenda_frame,
            text="Casa",
            fg_color='#00bf63',
            corner_radius=5,
            width=10,
            text_color='white',
            font=('system', 18, 'bold')
        )
        casa_legenda.grid(row=2, column=0, padx=5)

        feira_legenda = ctk.CTkLabel(
            legenda_frame,
            text="Feira",
            fg_color='#bf1900',
            corner_radius=5,
            width=10,
            text_color='white',
            font=('system', 18, 'bold')
        )
        feira_legenda.grid(row=2, column=1, padx=5)
