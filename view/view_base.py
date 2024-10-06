import customtkinter as ctk
from PIL import Image
from view.view_dados_cadastrais import DadosCadastrais


class FrameNavegacao(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='#00bf63', corner_radius=0)
        self.grid_columnconfigure(0)
        for i in range(5):
            self.grid_rowconfigure(i)
        self.grid_rowconfigure(4, weight=1)

        self.map_telas = {
            'home': None,
            'usuario': DadosCadastrais,
            'cestas': None,
        }

        icone_home = ctk.CTkImage(light_image=Image.open("./assets/icone_home.png"), size=(40, 40))
        self.botao_home = ctk.CTkButton(
            self,
            image=icone_home,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: self.alternar_tela('home')
        )
        self.botao_home.grid(row=0, column=0, sticky="ew")

        icone_usuario = ctk.CTkImage(light_image=Image.open("./assets/icone_usuario.png"), size=(40, 40))
        self.botao_usuario = ctk.CTkButton(self,
            image=icone_usuario,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: self.alternar_tela('usuario')
        )
        self.botao_usuario.grid(row=1, column=0, sticky="ew")

        icone_cesta = ctk.CTkImage(light_image=Image.open("./assets/icone_cesta.png"), size=(40, 40))
        self.botao_cesta = ctk.CTkButton(self,
            image=icone_cesta,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80,
            command=lambda: self.alternar_tela('cestas')
        )
        self.botao_cesta.grid(row=2, column=0, sticky="ew")

        icone_logout = ctk.CTkImage(light_image=Image.open("./assets/icone_logout.png"), size=(40, 40))
        self.botao_logout = ctk.CTkButton(self,
            image=icone_logout,
            text="",
            compound="left",
            fg_color='#00bf63',
            width=80,
            height=80
        )
        self.botao_logout.grid(row=3, column=0, sticky="ew")

    def alternar_tela(self, tela: str):
        self.master.frame.grid_forget()
        if self.map_telas[tela]:
            self.master.frame = self.map_telas[tela](self.master)
            self.master.frame.grid(column=1, row=0, padx=25, pady=25, sticky="nsew")


class ViewBase(ctk.CTkFrame):

    def __init__(self, master, controller_main):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_columnconfigure(0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2)
        self.grid_rowconfigure(0, weight=1)

        self.navegacao = FrameNavegacao(self)
        self.navegacao.grid(column=0, row=0, sticky="nsew")

        self.frame = DadosCadastrais(self)
        self.frame.grid(column=1, row=0, padx=25, pady=25, sticky="nsew")

        tem_feira_logo = Image.open('./assets/logo_tem_feira.png')
        self.tem_feira_logo = ctk.CTkImage(light_image=tem_feira_logo, size=(90, 60))
        self.tem_feira_logo_lbl = ctk.CTkLabel(self, image=self.tem_feira_logo, text='')
        self.tem_feira_logo_lbl.grid(column=2, row=0, padx=(0, 15), pady=15, sticky="new")
