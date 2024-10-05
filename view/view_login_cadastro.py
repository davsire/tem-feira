import customtkinter as ctk
from PIL import Image
from view.view_utils import ViewUtils
from view.frame_dados_feirante import FrameDadosFeirante


class FrameLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class FrameCadastro(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2)
        self.grid_rowconfigure(3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.label_cadastro = ctk.CTkLabel(self, text='Cadastro', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='w')

        tabview = ctk.CTkTabview(
            self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white',
        )
        tabview.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        tabview.add("Cliente")
        tabview.add("Feirante")
        tabview.set("Feirante")

        self.frame_feirante = FrameDadosFeirante(tabview.tab("Feirante"))
        self.frame_feirante.pack(fill="both", expand=True)

        self.botao_cadastrar = ViewUtils.obter_botao(self, 'Cadastrar')
        self.botao_cadastrar.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        self.label_tem_conta = ctk.CTkLabel(self, text='Já Tem conta? Faça login!', text_color='#38b6ff', font=('system', 18, 'bold'))
        self.label_tem_conta.grid(row=3, column=0, columnspan=2, pady=(0, 20))


class ViewLoginCadastro(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        tem_feira_img = Image.open('./assets/tem_feira.png')
        self.tem_feira_img = ctk.CTkImage(light_image=tem_feira_img, size=(400, 720))
        self.tem_feira_img_lbl = ctk.CTkLabel(self, image=self.tem_feira_img, text='')
        self.tem_feira_img_lbl.grid(column=1)

        self.frame = FrameCadastro(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
