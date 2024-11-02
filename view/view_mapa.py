import customtkinter as ctk
from tkintermapview import TkinterMapView
from model.feirante import Feirante
from view.frame.frame_detalhes_feirante import FrameDetalhesFeirante
from view.view_utils import ViewUtils


class ViewMapa(ctk.CTkFrame):

    def __init__(self, master, controller_main):
        super().__init__(master)
        self.__controller_main = controller_main
        self.__modal_feira: ctk.CTkToplevel | None = None

        self.configure(fg_color='white', corner_radius=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.busca_input = ctk.CTkEntry(self, placeholder_text='Buscar feira pelo nome...', height=35)
        self.busca_input.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        self.busca_input.bind('<Return>', command=lambda e: self.buscar_feirante())
        self.busca_botao = ViewUtils.obter_botao(self, 'Buscar')
        self.busca_botao.grid(row=0, column=1, sticky='ew', pady=(0, 15), padx=(10, 0))
        self.busca_botao.configure(height=35, command=self.buscar_feirante)

        self.mapa = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.mapa.grid(row=1, column=0, columnspan=2, sticky='nsew')

        latitude, longitude = self.__controller_main.obter_localizacao_usuario_logado()
        self.mapa.set_position(latitude, longitude)
        self.mapa.set_zoom(12)

        self.plotar_feiras()
        self.plotar_usuario_logado()
        self.criar_legenda()

    def plotar_feiras(self):
        feirantes = self.__controller_main.obter_feirantes()
        for feirante in feirantes:
            marker = self.mapa.set_marker(
                feirante.localizacao.latitude, feirante.localizacao.longitude,
                text=feirante.nome_feira, marker_color_circle='red', marker_color_outside='#bf1900',
                command=self.abrir_acoes_feira,
            )
            marker.data = feirante

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
        casa_legenda.grid(row=2, column=0, padx=(0, 5))

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

    def buscar_feirante(self):
        if not self.busca_input.get():
            return
        feirante = self.__controller_main.obter_feirante_por_nome(self.busca_input.get())
        if feirante is None:
            ViewUtils.abrir_popup_mensagem('Nenhuma feira encontrada...')
            return
        self.mapa.set_position(feirante.localizacao.latitude, feirante.localizacao.longitude)
        self.mapa.set_zoom(18)

    def abrir_acoes_feira(self, evento):
        feirante: Feirante = evento.data
        if self.__modal_feira is not None:
            self.__modal_feira.destroy()
        self.__modal_feira = ctk.CTkToplevel(self)
        self.__modal_feira.wm_geometry(f"+{self.winfo_pointerx() + 20}+{self.winfo_pointery() + 20}")
        self.__modal_feira.resizable(False, False)
        self.__modal_feira.attributes('-topmost', True)
        self.__modal_feira.configure(fg_color='white')
        self.__modal_feira.title(feirante.nome_feira)

        nome_feira = ctk.CTkLabel(self.__modal_feira, text=feirante.nome_feira, font=('system', 26, 'bold'))
        nome_feira.pack(padx=40, pady=30)

        botao_ver_feira = ViewUtils.obter_botao(self.__modal_feira, 'Ver feira')
        botao_ver_feira.configure(command=lambda: self.abrir_detalhes_feirante(feirante))
        botao_ver_feira.pack(padx=40, pady=(0, 30), fill='x')

        botao_como_chegar = ViewUtils.obter_botao(self.__modal_feira, 'Como chegar')
        botao_como_chegar.pack(padx=40, pady=(0, 30), fill='x')

        botao_fechar = ctk.CTkButton(self.__modal_feira, text='Fechar', fg_color='#bf1900', text_color='white', command=self.__modal_feira.destroy)
        botao_fechar.pack(padx=40, pady=(0, 30))

    def abrir_detalhes_feirante(self, feirante: Feirante):
        self.__modal_feira.destroy()
        self.__controller_main.abrir_tela_custom(FrameDetalhesFeirante, feirante)
