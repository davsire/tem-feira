import customtkinter as ctk
from PIL import Image
from view.view_dados_cadastrais import ViewDadosCadastrais
from view.view_detalhes_feirante import ViewDetalhesFeirante
from view.view_mapa import ViewMapa
from view.frame.frame_cadastro_produto import FrameCadastroProduto
from model.usuario import TipoUsuario



class FrameNavegacao(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='#00bf63', corner_radius=0)
        self.grid_columnconfigure(0)
        for i in range(5):
            self.grid_rowconfigure(i)
        self.grid_rowconfigure(4, weight=1)
        self.botoes = {}

        icone_home = ctk.CTkImage(light_image=Image.open("./assets/img/icone_home.png"), size=(40, 40))
        self.botoes['home'] = ctk.CTkButton(
            self,
            image=icone_home,
            text="",
            compound="left",
            fg_color='#bf1900',
            width=80,
            height=80,
            command=lambda: master.alternar_tela('home')
        )
        self.botoes['home'].grid(row=0, column=0, sticky="ew")

        icone_usuario = ctk.CTkImage(light_image=Image.open("./assets/img/icone_usuario.png"), size=(40, 40))
        self.botoes['usuario'] = ctk.CTkButton(self,
            image=icone_usuario,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: master.alternar_tela('usuario')
        )
        self.botoes['usuario'].grid(row=1, column=0, sticky="ew")

        icone_cesta = ctk.CTkImage(light_image=Image.open("./assets/img/icone_cesta.png"), size=(40, 40))
        self.botoes['cestas'] = ctk.CTkButton(self,
            image=icone_cesta,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: master.alternar_tela('cestas')
        )
        self.botoes['cestas'].grid(row=2, column=0, sticky="ew")

        icone_logout = ctk.CTkImage(light_image=Image.open("./assets/img/icone_logout.png"), size=(40, 40))
        self.botoes['logout'] = ctk.CTkButton(self,
            image=icone_logout,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: master.logout()
        )
        self.botoes['logout'].grid(row=3, column=0, pady=10, sticky="sew")
        
        icone_cadastro_produto = ctk.CTkImage(light_image=Image.open("./assets/img/icone-produto.png"), size=(40, 40))
        self.botoes['cadastro_produto'] = ctk.CTkButton(self,
            image=icone_cadastro_produto,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: master.alternar_tela('cadastro_produto')
        )
        self.botoes['cadastro_produto'].grid(row=3, column=0, sticky="ew")

    def selecionar_botao(self, botao: str):
        for b in list(self.botoes.values()):
            b.configure(fg_color='#00bf63')
        self.botoes[botao].configure(fg_color='#bf1900')


class FrameCustom(ctk.CTkFrame):
    def __init__(self, master, controller_main, tela, *args):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)

        self.botao_voltar = ctk.CTkButton(
            self,
            text='Voltar',
            fg_color='white',
            text_color="black",
            width=20,
            font=('system', 20, 'bold'),
            command=lambda: master.alternar_tela(master.tela_atual)
        )
        self.botao_voltar.grid(row=0, column=0, pady=(0, 20), sticky="w")

        self.tela = tela(self, controller_main, *args)
        self.tela.grid(row=1, column=0, sticky="nsew")


class ViewBase(ctk.CTkFrame):

    def __init__(self, master, controller_main):
        super().__init__(master)
        self.__controller_main = controller_main
        self.configure(fg_color='white')
        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2)
        self.grid_rowconfigure(0, weight=1)

        self.tela_atual = 'home'
        self.map_telas = {
            'home': ViewMapa if self.__controller_main.tipo_usuario_logado == TipoUsuario.CLIENTE else ViewDetalhesFeirante,
            'usuario': ViewDadosCadastrais,
            'cestas': None,
            'cadastro_produto': FrameCadastroProduto
        }

        self.navegacao = FrameNavegacao(self)
        self.navegacao.grid(column=0, row=0, sticky="nsew")

        self.frame = self.map_telas[self.tela_atual](self, self.__controller_main)
        self.frame.grid(column=1, row=0, padx=25, pady=25, sticky="nsew")

        tem_feira_logo = Image.open('./assets/img/logo_tem_feira.png')
        self.tem_feira_logo = ctk.CTkImage(light_image=tem_feira_logo, size=(90, 60))
        self.tem_feira_logo_lbl = ctk.CTkLabel(self, image=self.tem_feira_logo, text='')
        self.tem_feira_logo_lbl.grid(column=2, row=0, padx=(0, 15), pady=15, sticky="new")

    def alternar_tela(self, tela: str):
        self.tela_atual = tela
        self.frame.grid_forget()
        self.navegacao.selecionar_botao(tela)
        if self.map_telas[tela]:
            self.frame = self.map_telas[tela](self, self.__controller_main)
            self.frame.grid(column=1, row=0, padx=25, pady=25, sticky="nsew")

    def abrir_tela_custom(self, tela, *args):
        self.frame.grid_forget()
        self.frame = FrameCustom(self, self.__controller_main, tela, *args)
        self.frame.grid(column=1, row=0, padx=25, pady=25, sticky="nsew")

    def logout(self):
        self.__controller_main.logout()
