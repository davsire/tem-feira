import customtkinter as ctk
from view.frame_dados_feirante import FrameDadosFeirante
from view.view_utils import ViewUtils


class DadosCadastrais(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='white', corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2)

        self.label_cadastro = ctk.CTkLabel(self, text='Dados cadastrais', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro.grid(row=0, column=0, pady=(0, 30), sticky='w')

        self.frame_dados = FrameDadosFeirante(self)
        self.frame_dados.grid(row=1, column=0, columnspan=2, sticky='new')

        self.botao_salvar = ViewUtils.obter_botao(self, 'Salvar')
        self.botao_salvar.grid(column=0, row=2, sticky='w')

        self.botao_excluir_conta = ViewUtils.obter_botao(self, 'Excluir conta', '#e21515')
        self.botao_excluir_conta.grid(column=0, row=2, padx=(140,0), pady=20, sticky='w')
