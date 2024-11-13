# FILE: view/frame/frame_cadastro_produto.py
import customtkinter as ctk
from model.produto import UnidadeProduto
from view.view_utils import ViewUtils

class FrameCadastroProduto(ctk.CTkFrame):
    def _init_(self, master, controller_main):
        super()._init_(master)
        self.controller_main = controller_main
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2)
        self.grid_rowconfigure(3)
        self.grid_rowconfigure(4)
        self.grid_rowconfigure(5)
        self.grid_rowconfigure(6)
        self.grid_rowconfigure(7)
        self.grid_rowconfigure(8)
        
        self.nome_label = ctk.CTkLabel(self, text='Nome do Produto *', font=('system', 20))
        self.nome_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite o nome do produto')
        self.nome_label.grid(row=0, column=0, columnspan=2, sticky='w')
        self.nome_entry.grid(row=1, column=0, columnspan=2, sticky='new')

        self.preco_label = ctk.CTkLabel(self, text='Preço *', font=('system', 20))
        self.preco_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite o preço do produto')
        self.preco_label.grid(row=2, column=0, columnspan=2, sticky='w')
        self.preco_entry.grid(row=3, column=0, columnspan=2, sticky='new')

        self.quantidade_label = ctk.CTkLabel(self, text='Quantidade *', font=('system', 20))
        self.quantidade_entry = ctk.CTkEntry(self, height=40, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label.grid(row=4, column=0, columnspan=2, sticky='w')
        self.quantidade_entry.grid(row=5, column=0, columnspan=2, sticky='new')

        self.unidade_label = ctk.CTkLabel(self, text='Unidade *', font=('system', 20))
        self.unidade_combobox = ctk.CTkComboBox(self, values=[unidade.value for unidade in UnidadeProduto], height=40)
        self.unidade_label.grid(row=6, column=0, columnspan=2, sticky='w')
        self.unidade_combobox.grid(row=7, column=0, columnspan=2, sticky='new')

        self.botao_cadastrar = ViewUtils.obter_botao(self, 'Cadastrar Produto')
        self.botao_cadastrar.configure(command=self.cadastrar_produto)
        self.botao_cadastrar.grid(row=8, column=0, columnspan=2, pady=(20, 0))

    def cadastrar_produto(self):
        dados = {
            'nome': self.nome_entry.get(),
            'preco': float(self.preco_entry.get()),
            'quantidade': float(self.quantidade_entry.get()),
            'unidade': self.unidade_combobox.get(),
            'feirante': self.controller_main.usuario_logado.to_dict()
        }
        self.controller_main.controller_produto.criar_produto(dados)
        ViewUtils.abrir_popup_mensagem('Produto cadastrado com sucesso!', 'green')