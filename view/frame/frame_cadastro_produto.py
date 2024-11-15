import customtkinter as ctk
from model.produto import UnidadeProduto
from view.view_utils import ViewUtils
from PIL import Image, ImageTk
from bson import ObjectId

class FrameCadastroProduto(ctk.CTkFrame):
    def __init__(self, master, controller_main):
        super().__init__(master)
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
        self.grid_rowconfigure(9)

        # Load and display the image using CTkImage
        image_path = 'assets/img/produto_default.png'
        self.image = Image.open(image_path)
        self.ctk_image = ctk.CTkImage(self.image, size=(100, 100))
        self.image_label = ctk.CTkLabel(self, image=self.ctk_image, text='')
        self.image_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.tabview = ctk.CTkTabview(self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white')
        
        self.tabview.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 20), sticky='nsew')
        self.tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        self.tabview.add("Cadastro")
        self.tabview.add("Edição")

        self.create_cadastro_tab()
        self.create_edicao_tab()

    def create_cadastro_tab(self):
        tab = self.tabview.tab("Cadastro")
        self.nome_label = ctk.CTkLabel(tab, text='Nome do Produto *', font=('system', 16))
        self.nome_entry = ctk.CTkEntry(tab, height=30, placeholder_text='Digite o nome do produto')
        self.nome_label.grid(row=1, column=0, columnspan=2, sticky='w')
        self.nome_entry.grid(row=2, column=0, columnspan=2, sticky='new')

        self.preco_label = ctk.CTkLabel(tab, text='Preço *', font=('system', 16))
        self.preco_entry = ctk.CTkEntry(tab, height=30, placeholder_text='Digite o preço do produto')
        self.preco_label.grid(row=3, column=0, columnspan=2, sticky='w')
        self.preco_entry.grid(row=4, column=0, columnspan=2, sticky='new')

        self.quantidade_label = ctk.CTkLabel(tab, text='Quantidade *', font=('system', 16))
        self.quantidade_entry = ctk.CTkEntry(tab, height=30, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label.grid(row=5, column=0, columnspan=2, sticky='w')
        self.quantidade_entry.grid(row=6, column=0, columnspan=2, sticky='new')

        self.unidade_label = ctk.CTkLabel(tab, text='Unidade *', font=('system', 16))
        self.unidade_combobox = ctk.CTkComboBox(tab, values=[unidade.name for unidade in UnidadeProduto], height=30)
        self.unidade_label.grid(row=7, column=0, columnspan=2, sticky='w')
        self.unidade_combobox.grid(row=8, column=0, columnspan=2, sticky='new')

        self.botao_cadastrar = ViewUtils.obter_botao(tab, 'Cadastrar Produto')
        self.botao_cadastrar.configure(command=self.cadastrar_produto)
        self.botao_cadastrar.grid(row=9, column=0, pady=(20, 0), sticky='e')

    def create_edicao_tab(self):
        tab = self.tabview.tab("Edição")
        
        self.produto_combobox = ctk.CTkComboBox(tab, values=self.obter_nomes_produtos(), height=30)
        self.produto_combobox.grid(row=0, column=0, columnspan=2, sticky='new')
        self.produto_combobox.bind("<<Selecione o produto>>", self.carregar_dados_produto)

        self.preco_label_edicao = ctk.CTkLabel(tab, text='Preço *', font=('system', 16))
        self.preco_entry_edicao = ctk.CTkEntry(tab, height=30, placeholder_text='Digite o preço do produto')
        self.preco_label_edicao.grid(row=3, column=0, columnspan=2, sticky='w')
        self.preco_entry_edicao.grid(row=4, column=0, columnspan=2, sticky='new')

        self.quantidade_label_edicao = ctk.CTkLabel(tab, text='Quantidade *', font=('system', 16))
        self.quantidade_entry_edicao = ctk.CTkEntry(tab, height=30, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label_edicao.grid(row=5, column=0, columnspan=2, sticky='w')
        self.quantidade_entry_edicao.grid(row=6, column=0, columnspan=2, sticky='new')

        self.unidade_label_edicao = ctk.CTkLabel(tab, text='Unidade *', font=('system', 16))
        self.unidade_combobox_edicao = ctk.CTkComboBox(tab, values=[unidade.name for unidade in UnidadeProduto], height=30)
        self.unidade_label_edicao.grid(row=7, column=0, columnspan=2, sticky='w')
        self.unidade_combobox_edicao.grid(row=8, column=0, columnspan=2, sticky='new')

        # Frame para os botões
        frame_botoes = ctk.CTkFrame(tab, fg_color='transparent')
        frame_botoes.grid(row=9, column=0, columnspan=2, pady=(20, 0), sticky='e')
        
        # Botão Excluir (vermelho)
        self.botao_excluir = ViewUtils.obter_botao(
            frame_botoes, 
            'Excluir', 
            fg_color='#bf1900',
            text_color='white'
        )
        self.botao_excluir.configure(command=self.excluir_produto)
        self.botao_excluir.pack(side='left', padx=(0, 10))
        
        # Botão Editar (verde)
        self.botao_editar = ViewUtils.obter_botao(
            frame_botoes, 
            'Editar',
            fg_color='#00bf63',
            text_color='white'
        )
        self.botao_editar.configure(command=self.editar_produto)
        self.botao_editar.pack(side='left')
        

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

    def obter_nomes_produtos(self):
        # Obter apenas os produtos do feirante logado
        feirante_id = self.controller_main.usuario_logado.id
        produtos = self.controller_main.controller_produto.obter_produtos_por_feirante(feirante_id, False)
        return [produto.nome for produto in produtos]

    def cadastrar_produto(self):
        nome = self.nome_entry.get().lower()  # Converte o nome para minúsculas
        preco = float(self.preco_entry.get())
        quantidade = float(self.quantidade_entry.get())
        unidade = self.unidade_combobox.get()
        
        produtos_kg = [
            'abacate', 'abacaxi', 'abobrinha', 'abóbora', 'aipo', 'alho', 'almeirão', 'ameixa', 'amora', 'aspargo',
            'banana', 'batata', 'batata-doce', 'berinjela', 'beterraba', 'brócolis', 'caju', 'caqui', 'carambola', 'cebola',
            'cenoura', 'cereja', 'chuchu', 'couve', 'couve-flor', 'damasco', 'ervilha', 'espinafre', 'figo', 'framboesa',
            'gengibre', 'goiaba', 'graviola', 'inhame', 'jaca', 'jiló', 'kiwi', 'laranja', 'limão', 'maçã', 'mamão', 'manga',
            'maracujá', 'melancia', 'melão', 'morango', 'nectarina', 'nêspera', 'pepino', 'pêssego', 'pimentão', 'quiabo',
            'rabanete', 'repolho', 'rúcula', 'salsa', 'tangerina', 'tomate', 'uva'
        ]

        produtos_unidade = [
            'pote de mel', 'garrafa de suco', 'pacote de biscoito', 'barra de chocolate', 'caixa de ovos', 'pote de geleia',
            'garrafa de azeite', 'pote de iogurte', 'caixa de leite', 'garrafa de água'
        ]

        if nome in produtos_kg and unidade != 'KG':
            ViewUtils.abrir_popup_mensagem('Este produto deve ser cadastrado na unidade KG.', 'red')
            return

        if nome in produtos_unidade and unidade != 'UNIDADE':
            ViewUtils.abrir_popup_mensagem('Este produto deve ser cadastrado na unidade UNIDADE.', 'red')
            return
        
        feirante = self.controller_main.usuario_logado.to_dict()
        feirante['_id'] = self.controller_main.usuario_logado.id
        
        # Verificar se o produto já existe
        produto_existente = self.controller_main.controller_produto.obter_produto_por_nome_e_feirante(nome, feirante['_id'])
        if produto_existente:
            ViewUtils.abrir_popup_mensagem('Este produto já existe no seu catálogo!', 'red')
            return
        
        dados = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'unidade': unidade,
            'feirante': feirante
        }
        
        self.controller_main.controller_produto.salvar_produto(dados)
        ViewUtils.abrir_popup_mensagem('Produto salvo com sucesso!', 'green')
        def upload_imagem_produto(self):
            file_path = ctk.filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
            )
            if file_path:
                self.image = Image.open(file_path)
                self.ctk_image = ctk.CTkImage(self.image, size=(100, 100))
                self.image_label.configure(image=self.ctk_image)
                self.image_path = file_path

        self.botao_upload_imagem = ViewUtils.obter_botao(self, 'Upload Imagem')
        self.botao_upload_imagem.configure(command=self.upload_imagem_produto)
        self.botao_upload_imagem.grid(row=10, column=0, pady=(20, 0), sticky='e')

    def editar_produto(self):
        nome = self.produto_combobox.get()  # Obtém o nome do produto selecionado no combobox
        preco = float(self.preco_entry_edicao.get())
        quantidade = float(self.quantidade_entry_edicao.get())
        unidade = self.unidade_combobox_edicao.get()
        feirante = self.controller_main.usuario_logado.to_dict()
        feirante['_id'] = self.controller_main.usuario_logado.id
        
        
        produtos_kg = [
            'abacate', 'abacaxi', 'abobrinha', 'abóbora', 'aipo', 'alho', 'almeirão', 'ameixa', 'amora', 'aspargo',
            'banana', 'batata', 'batata-doce', 'berinjela', 'beterraba', 'brócolis', 'caju', 'caqui', 'carambola', 'cebola',
            'cenoura', 'cereja', 'chuchu', 'couve', 'couve-flor', 'damasco', 'ervilha', 'espinafre', 'figo', 'framboesa',
            'gengibre', 'goiaba', 'graviola', 'inhame', 'jaca', 'jiló', 'kiwi', 'laranja', 'limão', 'maçã', 'mamão', 'manga',
            'maracujá', 'melancia', 'melão', 'morango', 'nectarina', 'nêspera', 'pepino', 'pêssego', 'pimentão', 'quiabo',
            'rabanete', 'repolho', 'rúcula', 'salsa', 'tangerina', 'tomate', 'uva'
            ]# Substitua pelos nomes reais dos produtos

        produtos_unidade = [
            'pote de mel', 'garrafa de suco', 'pacote de biscoito', 'barra de chocolate', 'caixa de ovos', 'pote de geleia',
            'garrafa de azeite', 'pote de iogurte', 'caixa de leite', 'garrafa de água'
        ]

        if nome in produtos_kg and unidade != 'KG':
            ViewUtils.abrir_popup_mensagem('Este produto deve ser cadastrado na unidade KG.', 'red')
            return

        if nome in produtos_unidade and unidade != 'UNIDADE':
            ViewUtils.abrir_popup_mensagem('Este produto deve ser cadastrado na unidade UNIDADE.', 'red')
            return
        
        dados = {
            'nome': nome,
            'preco': preco,
            'quantidade': quantidade,
            'unidade': unidade,
            'feirante': feirante
        }
        
        self.controller_main.controller_produto.editar_produto(dados)
        ViewUtils.abrir_popup_mensagem('Produto editado com sucesso!', 'green')
        
    def excluir_produto(self):
        """Exclui o produto selecionado após confirmação"""
        nome = self.produto_combobox.get()
        if not nome:
            ViewUtils.abrir_popup_mensagem('Selecione um produto para excluir!', 'red')
            return
            
        feirante_id = self.controller_main.usuario_logado.id
        produto = self.controller_main.controller_produto.obter_produto_por_nome_e_feirante(nome, feirante_id)
        
        if produto:
            def confirmar_exclusao():
                self.controller_main.controller_produto.excluir_produto(produto.id)
                # Atualiza a lista de produtos
                self.produto_combobox.configure(values=self.obter_nomes_produtos())
                # Limpa os campos
                self.produto_combobox.set('')
                self.preco_entry_edicao.delete(0, 'end')
                self.quantidade_entry_edicao.delete(0, 'end')
                ViewUtils.abrir_popup_mensagem('Produto excluído com sucesso!', 'green')
                
            ViewUtils.abrir_popup_confirmacao(
                'Tem certeza que deseja excluir este produto?',
                'Excluir',
                confirmar_exclusao,
                '#bf1900'
            )