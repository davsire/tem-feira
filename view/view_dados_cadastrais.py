import customtkinter as ctk
from model.usuario import TipoUsuario
from view.frame.frame_dados_cliente import FrameDadosCliente
from view.frame.frame_dados_feirante import FrameDadosFeirante
from view.view_utils import ViewUtils


class ViewDadosCadastrais(ctk.CTkFrame):

    def __init__(self, master, controller_main):
        super().__init__(master)
        self.__controller_main = controller_main
        self.configure(fg_color='white', corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2)

        self.label_cadastro = ctk.CTkLabel(self, text='Dados cadastrais', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro.grid(row=0, column=0, pady=(0, 30), sticky='w')

        self.frame_dados: FrameDadosFeirante | FrameDadosCliente = self.obter_frame_dados()
        self.frame_dados.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.botao_salvar = ViewUtils.obter_botao(self, 'Salvar')
        self.botao_salvar.configure(command=self.atualizar_conta)
        self.botao_salvar.grid(column=0, row=2, sticky='w')

        self.botao_excluir_conta = ViewUtils.obter_botao(self, 'Excluir conta', '#bf1900')
        self.botao_excluir_conta.configure(command=self.excluir_conta)
        self.botao_excluir_conta.grid(column=0, row=2, padx=(140,0), pady=20, sticky='w')

    def obter_frame_dados(self) -> FrameDadosFeirante | FrameDadosCliente:
        if self.__controller_main.tipo_usuario_logado == TipoUsuario.FEIRANTE:
            return FrameDadosFeirante(self, self.__controller_main.usuario_logado)
        if self.__controller_main.tipo_usuario_logado == TipoUsuario.CLIENTE:
            return FrameDadosCliente(self, self.__controller_main.usuario_logado)

    def atualizar_conta(self):
        dados = None
        if self.__controller_main.tipo_usuario_logado == TipoUsuario.FEIRANTE:
            dados = self.frame_dados.obter_dados_feirante()
        if self.__controller_main.tipo_usuario_logado == TipoUsuario.CLIENTE:
            dados = self.frame_dados.obter_dados_cliente()
        self.__controller_main.atualizar_usuario(dados)

    def excluir_conta(self):
        self.__controller_main.confirmar_exclusao_conta()
