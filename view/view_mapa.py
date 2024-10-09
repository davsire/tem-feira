# view/view_mapa.py
import customtkinter as ctk
from tkintermapview import TkinterMapView
from controller.controller_mapa import ControllerMapa

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
        
        # Centralize o mapa em Florianópolis
        self.mapa.set_position(-27.5954, -48.5480)  # Coordenadas de Florianópolis
        self.mapa.set_zoom(12)  # Ajuste o nível de zoom conforme necessário
        
        self.controller_mapa = ControllerMapa()
        self.plotar_feiras()
        self.plotar_usuario_logado()
        
        self.criar_legenda()

    def plotar_feiras(self):
        localizacoes = self.controller_mapa.obter_localizacoes_feirantes()
        for nome_feira, latitude, longitude in localizacoes:
            self.mapa.set_marker(latitude, longitude, text=nome_feira, marker_color_circle='red', marker_color_outside='darkred')
        
    def plotar_usuario_logado(self):
        coordenada_usuario = self.__controller_main.obter_coordenada_usuario_logado()
        if coordenada_usuario:
            latitude, longitude = coordenada_usuario
            # Outra forma de fazer um marker é utilizando o método `add_marker`
            self.mapa.set_marker(latitude, longitude, text="Sua casa", marker_color_circle='#90EE90', marker_color_outside='#00bf63')  # Light green color

    def criar_legenda(self):
        legenda_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=0)
        legenda_frame.grid(row=2, column=0, sticky='ew', pady=10)
        
        feira_legenda = ctk.CTkLabel(legenda_frame, text="Feira", fg_color='red', corner_radius=5, width=10)
        feira_legenda.grid(row=2, column=0, padx=5)
        
        casa_legenda = ctk.CTkLabel(legenda_frame, text="Casa", fg_color='#90EE90', corner_radius=5, width=10)
        casa_legenda.grid(row=2, column=1, padx=5)