import customtkinter as ctk
from model.produto import UnidadeProduto
from view.view_utils import ViewUtils
from PIL import Image, ImageTk
from bson import ObjectId
from tkinter import filedialog
import os

class FrameCadastroProduto(ctk.CTkFrame):
    def __init__(self, master, controller_main):
        super().__init__(master)
        self.controller_main = controller_main
        self.configure(fg_color='white')
        self.imagem_path = None
        self.imagem_path_edicao = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)

        self.label_cadastro_edicao = ctk.CTkLabel(self, text='Cadastro/Edição de produto', text_color='black', font=('system', 35, 'bold'))
        self.label_cadastro_edicao.grid(row=0, column=0, pady=(0, 30), sticky='w')
        self.tabview = ctk.CTkTabview(self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white')
        
        self.tabview.grid(row=1, column=0, padx=40, pady=(20, 20), sticky='nsew')
        self.tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        self.tabview.add("Cadastro")
        self.tabview.add("Edição")

        self.create_cadastro_tab()
        self.create_edicao_tab()
        
    def create_edicao_tab(self):
        tab = self.tabview.tab("Edição")
        tab.grid_columnconfigure(0, weight=1)

        self.produto_label = ctk.CTkLabel(tab, text='Produto *', font=('system', 16))
        self.produto_combobox = ctk.CTkComboBox(tab, values=self.obter_nomes_produtos(), height=40)
        self.produto_label.grid(row=0, column=0, sticky='w')
        self.produto_combobox.grid(row=1, column=0, sticky='new', pady=(0, 10))
        self.produto_combobox.bind("<<ComboboxSelected>>", self.carregar_dados_produto)
        
        self.preco_label_edicao = ctk.CTkLabel(tab, text='Preço *', font=('system', 16))
        self.preco_entry_edicao = ctk.CTkEntry(tab, height=40, placeholder_text='Digite o preço do produto')
        self.preco_label_edicao.grid(row=2, column=0, sticky='w')
        self.preco_entry_edicao.grid(row=3, column=0, sticky='new', pady=(0, 10))
        
        self.quantidade_label_edicao = ctk.CTkLabel(tab, text='Quantidade *', font=('system', 16))
        self.quantidade_entry_edicao = ctk.CTkEntry(tab, height=40, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label_edicao.grid(row=4, column=0, sticky='w')
        self.quantidade_entry_edicao.grid(row=5, column=0, sticky='new', pady=(0, 10))
        
        self.unidade_label_edicao = ctk.CTkLabel(tab, text='Unidade *', font=('system', 16))
        self.unidade_combobox_edicao = ctk.CTkComboBox(tab, values=[unidade.name for unidade in UnidadeProduto], height=40)
        self.unidade_label_edicao.grid(row=6, column=0, sticky='w')
        self.unidade_combobox_edicao.grid(row=7, column=0, sticky='new', pady=(0, 10))

        frame_imagem_edicao = ctk.CTkFrame(tab, fg_color='transparent')
        frame_imagem_edicao.grid(row=8, column=0, pady=(10, 0), sticky='ew')

        self.botao_upload_edicao = ViewUtils.obter_botao(
            frame_imagem_edicao,
            'Escolher Imagem',
            fg_color='#4a90e2',
            text_color='white'
        )
        self.botao_upload_edicao.configure(command=self.escolher_imagem_edicao)
        self.botao_upload_edicao.pack(side='left')

        self.label_imagem_edicao = ctk.CTkLabel(frame_imagem_edicao, text='Nenhuma imagem selecionada', font=('system', 12))
        self.label_imagem_edicao.pack(side='left', padx=(10, 0))

        frame_botoes = ctk.CTkFrame(tab, fg_color='transparent')
        frame_botoes.grid(row=9, column=0, pady=(20, 0), sticky='ew')

        self.botao_editar = ViewUtils.obter_botao(frame_botoes, 'Salvar')
        self.botao_editar.configure(command=self.editar_produto)
        self.botao_editar.pack(side='left', padx=(0, 10))

        self.botao_excluir = ViewUtils.obter_botao(frame_botoes, 'Excluir produto', fg_color='#bf1900', text_color='white')
        self.botao_excluir.configure(command=self.excluir_produto)
        self.botao_excluir.pack(side='left')

    def create_cadastro_tab(self):
        tab = self.tabview.tab("Cadastro")
        tab.grid_columnconfigure(0, weight=1)

        self.nome_label = ctk.CTkLabel(tab, text='Nome do Produto *', font=('system', 16))
        self.nome_entry = ctk.CTkEntry(tab, height=40, placeholder_text='Digite o nome do produto')
        self.nome_label.grid(row=1, column=0, sticky='w')
        self.nome_entry.grid(row=2, column=0, sticky='new', pady=(0, 10))

        self.preco_label = ctk.CTkLabel(tab, text='Preço *', font=('system', 16))
        self.preco_entry = ctk.CTkEntry(tab, height=40, placeholder_text='Digite o preço do produto')
        self.preco_label.grid(row=3, column=0, sticky='w')
        self.preco_entry.grid(row=4, column=0, sticky='new', pady=(0, 10))

        self.quantidade_label = ctk.CTkLabel(tab, text='Quantidade *', font=('system', 16))
        self.quantidade_entry = ctk.CTkEntry(tab, height=40, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label.grid(row=5, column=0, sticky='w')
        self.quantidade_entry.grid(row=6, column=0, sticky='new', pady=(0, 10))

        self.unidade_label = ctk.CTkLabel(tab, text='Unidade *', font=('system', 16))
        self.unidade_combobox = ctk.CTkComboBox(tab, values=[unidade.name for unidade in UnidadeProduto], height=40)
        self.unidade_label.grid(row=7, column=0, sticky='w')
        self.unidade_combobox.grid(row=8, column=0, sticky='new', pady=(0, 10))

        frame_imagem = ctk.CTkFrame(tab, fg_color='transparent')
        frame_imagem.grid(row=9, column=0, pady=(10, 0), sticky='ew')

        self.botao_upload = ViewUtils.obter_botao(
            frame_imagem,
            'Escolher Imagem',
            fg_color='#4a90e2',
            text_color='white'
        )
        self.botao_upload.configure(command=self.escolher_imagem)
        self.botao_upload.pack(side='left')

        self.label_imagem = ctk.CTkLabel(frame_imagem, text='Nenhuma imagem selecionada', font=('system', 12))
        self.label_imagem.pack(side='left', padx=(10, 0))

        self.botao_cadastrar = ViewUtils.obter_botao(tab, 'Cadastrar produto')
        self.botao_cadastrar.configure(command=self.cadastrar_produto)
        self.botao_cadastrar.grid(row=10, column=0, pady=(20, 0), sticky='w')
    
    def escolher_imagem_edicao(self):
        filetypes = (
            ('Imagens', '*.png *.jpg *.jpeg'),
            ('Todos os arquivos', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Escolha uma imagem',
            initialdir='/',
            filetypes=filetypes
        )
        
        if filename:
            self.imagem_path_edicao = filename
            self.label_imagem_edicao.configure(text=os.path.basename(filename))
    
    def escolher_imagem(self):
        filetypes = (
            ('Imagens', '*.png *.jpg *.jpeg'),
            ('Todos os arquivos', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Escolha uma imagem',
            initialdir='/',
            filetypes=filetypes
        )
        
        if filename:
            self.imagem_path = filename
            self.label_imagem.configure(text=os.path.basename(filename))

    def carregar_dados_produto(self, event):
        nome_produto = self.produto_combobox.get()
        
        feirante = self.controller_main.usuario_logado.to_dict()
        feirante['_id'] = self.controller_main.usuario_logado.id
        feirante_id = feirante['_id']
        
        produto = self.controller_main.controller_produto.obter_produto_por_nome_e_feirante(nome_produto, feirante_id)
        if produto:
            self.preco_entry_edicao.delete(0, 'end')
            self.preco_entry_edicao.insert(0, produto['preco'])
            self.quantidade_entry_edicao.delete(0, 'end')
            self.quantidade_entry_edicao.insert(0, produto['quantidade'])
            self.unidade_combobox_edicao.set(produto['unidade'])
            self.imagem_path_edicao = produto['imagem']
            self.label_imagem_edicao.configure(text=os.path.basename(produto['imagem']))

    def obter_nomes_produtos(self):
        feirante_id = self.controller_main.usuario_logado.id
        produtos = self.controller_main.controller_produto.obter_produtos_por_feirante(feirante_id, False)
        return [produto.nome for produto in produtos]

    def cadastrar_produto(self):
        nome = self.nome_entry.get()
        preco = self.preco_entry.get().replace(',', '.')
        quantidade = self.quantidade_entry.get()
        unidade = self.unidade_combobox.get()
        feirante = self.controller_main.usuario_logado.to_dict()
        feirante['_id'] = self.controller_main.usuario_logado.id
        imagem = self.imagem_path if self.imagem_path else './assets/img/produto_default.png'
        
        dados = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'unidade': unidade,
            'feirante': feirante,
            'imagem': imagem
        }
        
        mensagem = self.controller_main.controller_produto.salvar_produto(dados)
        ViewUtils.abrir_popup_mensagem(mensagem, 'green' if 'sucesso' in mensagem else 'red')
        
        if 'sucesso' in mensagem:
            self.imagem_path = None
            self.label_imagem.configure(text='Nenhuma imagem selecionada')

    def editar_produto(self):
        nome = self.produto_combobox.get()
        preco = self.preco_entry_edicao.get().replace(',', '.')
        quantidade = self.quantidade_entry_edicao.get()
        unidade = self.unidade_combobox_edicao.get()
        feirante = self.controller_main.usuario_logado.to_dict()
        feirante['_id'] = self.controller_main.usuario_logado.id
        imagem = self.imagem_path_edicao if self.imagem_path_edicao else './assets/img/produto_default.png'
        
        dados = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'unidade': unidade,
            'feirante': feirante,
            'imagem': imagem
        }
        
        mensagem = self.controller_main.controller_produto.editar_produto(dados)
        ViewUtils.abrir_popup_mensagem(mensagem, 'green' if 'sucesso' in mensagem else 'red')
        
        if 'sucesso' in mensagem:
            self.imagem_path_edicao = None
            self.label_imagem_edicao.configure(text='Nenhuma imagem selecionada')
        
    def excluir_produto(self):
        nome = self.produto_combobox.get()
        if not nome:
            ViewUtils.abrir_popup_mensagem('Selecione um produto para excluir!', 'red')
            return
        feirante_id = self.controller_main.usuario_logado.id
        produto = self.controller_main.controller_produto.obter_produto_por_nome_e_feirante(nome, feirante_id)
        if produto:
            def confirmar_exclusao():
                mensagem = self.controller_main.controller_produto.excluir_produto(nome, feirante_id)
                if 'sucesso' in mensagem:
                    self.produto_combobox.configure(values=self.obter_nomes_produtos())
                    self.produto_combobox.set('')
                    self.preco_entry_edicao.delete(0, 'end')
                    self.quantidade_entry_edicao.delete(0, 'end')
                ViewUtils.abrir_popup_mensagem(mensagem, 'green' if 'sucesso' in mensagem else 'red')
            ViewUtils.abrir_popup_confirmacao(
                'Tem certeza que deseja excluir este produto?',
                'Excluir',
                confirmar_exclusao,
                '#bf1900'
            )
