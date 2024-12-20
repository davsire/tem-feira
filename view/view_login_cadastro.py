import customtkinter as ctk
from PIL import Image
from model.usuario import TipoUsuario
from view.view_utils import ViewUtils
from view.frame.frame_dados_feirante import FrameDadosFeirante
from view.frame.frame_dados_login import FrameDadosLogin
from view.frame.frame_dados_cliente import FrameDadosCliente


class FrameLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2)
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label_login = ctk.CTkLabel(self, text='Login', text_color='black', font=('system', 35, 'bold'))
        self.label_login.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='w')

        self.frame_login = FrameDadosLogin(self)
        self.frame_login.grid(row=1, column=0, columnspan=2, padx=300, stick='ew')

        self.botao_login = ViewUtils.obter_botao(self, 'Login')
        self.botao_login.configure(command=master.logar_usuario)
        self.botao_login.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        self.label_nao_tem_conta = ctk.CTkLabel(self, text='Não Tem conta? Clique para se cadastrar!', text_color='#38b6ff', font=('system', 18, 'bold'))
        self.label_nao_tem_conta.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        self.label_nao_tem_conta.bind('<Button-1>', lambda e: master.alternar_tela('cadastro'))

class FrameCadastro(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2)
        self.grid_rowconfigure(3)
        self.grid_rowconfigure(4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label_cadastro = ctk.CTkLabel(self, text='Cadastro', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro.grid(row=0, column=0, padx=20, pady=(20, 0), sticky='w')

        tabview = ctk.CTkTabview(
            self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white',
        )
        tabview.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        tabview.add(TipoUsuario.CLIENTE.value)
        tabview.add(TipoUsuario.FEIRANTE.value)
        tabview.set(TipoUsuario.CLIENTE.value)

        self.frame_feirante = FrameDadosFeirante(tabview.tab(TipoUsuario.FEIRANTE.value), None)
        self.frame_feirante.pack(fill="both", expand=True)

        self.frame_cliente = FrameDadosCliente(tabview.tab(TipoUsuario.CLIENTE.value), None)
        self.frame_cliente.pack(fill="both", expand=True)

        self.label_tem_conta = ctk.CTkLabel(self, text='* Campos obrigatórios', text_color='black', font=('system', 12, 'bold'))
        self.label_tem_conta.grid(row=2, column=0, columnspan=2, padx=(30, 0), sticky='w')

        self.botao_cadastrar = ViewUtils.obter_botao(self, 'Cadastrar')
        self.botao_cadastrar.configure(command=lambda: master.cadastrar_usuario(tabview.get()))
        self.botao_cadastrar.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        self.label_tem_conta = ctk.CTkLabel(self, text='Já Tem conta? Clique para fazer login!', text_color='#38b6ff', font=('system', 18, 'bold'))
        self.label_tem_conta.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        self.label_tem_conta.bind('<Button-1>', lambda e: master.alternar_tela('login'))


class ViewLoginCadastro(ctk.CTkFrame):

    def __init__(self, master, controller_main):
        super().__init__(master)
        self.__controller_main = controller_main
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.map_telas = {
            'login': FrameLogin,
            'cadastro': FrameCadastro,
        }

        tem_feira_img = Image.open('./assets/img/tem_feira.png')
        self.tem_feira_img = ctk.CTkImage(light_image=tem_feira_img, size=(400, 720))
        self.tem_feira_img_lbl = ctk.CTkLabel(self, image=self.tem_feira_img, text='')
        self.tem_feira_img_lbl.grid(column=1)

        self.frame: FrameLogin | FrameCadastro = FrameLogin(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        master.bind('<Return>', lambda e: self.logar_usuario() if isinstance(self.frame, FrameLogin) else None)

    def alternar_tela(self, tela: str):
        self.frame.grid_forget()
        if self.map_telas[tela]:
            self.frame = self.map_telas[tela](self)
            self.frame.grid(row=0, column=0, sticky="nsew")

    def cadastrar_usuario(self, tipo: str):
        dados = None
        tipo_usuario = TipoUsuario[tipo.upper()]
        if tipo_usuario == TipoUsuario.FEIRANTE:
            dados = self.frame.frame_feirante.obter_dados_feirante()
        if tipo_usuario == TipoUsuario.CLIENTE:
            dados = self.frame.frame_cliente.obter_dados_cliente()
        self.__controller_main.cadastrar_usuario(dados, tipo_usuario)

    def logar_usuario(self):
        dados = self.frame.frame_login.obter_dados_login()
        self.__controller_main.logar_usuario(dados)
