import customtkinter as ctk
from PIL import Image
from view.view_utils import ViewUtils


class FrameLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class FrameCadastro(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white', height=720)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3)
        self.grid_rowconfigure(4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label_cadastro = ctk.CTkLabel(self, text='Cadastro', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.botao_cliente = ViewUtils.obter_botao(self, 'Cliente')
        self.botao_cliente.grid(row=1, column=0, padx=(0, 20), sticky='e')
        self.botao_feirante = ViewUtils.obter_botao(self, 'Feirante')
        self.botao_feirante.grid(row=1, column=1, sticky='w')

        self.botao_cadastrar = ViewUtils.obter_botao(self, 'Cadastrar')
        self.botao_cadastrar.grid(row=3, column=0, columnspan=2, pady=(0, 15))

        self.label_tem_conta = ctk.CTkLabel(self, text='Já Tem conta? Faça login!', text_color='#38b6ff', font=('system', 18, 'bold'))
        self.label_tem_conta.grid(row=4, column=0, columnspan=2, pady=(0, 15))


class ViewLoginCadastro(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)

        tem_feira_img = Image.open('./assets/tem_feira.png')
        self.tem_feira_img = ctk.CTkImage(light_image=tem_feira_img, size=(400, 720))
        self.tem_feira_img_lbl = ctk.CTkLabel(self, image=self.tem_feira_img, text='')
        self.tem_feira_img_lbl.grid(column=1)

        self.frame = FrameCadastro(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
