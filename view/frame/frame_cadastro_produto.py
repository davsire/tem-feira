# FILE: view/frame/frame_cadastro_produto.py
import customtkinter as ctk
from model.produto import UnidadeProduto
from view.view_utils import ViewUtils
from PIL import Image, ImageTk

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
        image_path = '/home/ale-vasco/ale/UFSC/APS/tem-feira/assets/img/icone-produto.png'
        self.image = Image.open(image_path)
        self.ctk_image = ctk.CTkImage(self.image, size=(100, 100))
        self.image_label = ctk.CTkLabel(self, image=self.ctk_image, text='')
        self.image_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.nome_label = ctk.CTkLabel(self, text='Nome do Produto *', font=('system', 16))
        self.nome_entry = ctk.CTkEntry(self, height=30, placeholder_text='Digite o nome do produto')
        self.nome_label.grid(row=1, column=0, columnspan=2, sticky='w')
        self.nome_entry.grid(row=2, column=0, columnspan=2, sticky='new')

        self.preco_label = ctk.CTkLabel(self, text='Preço *', font=('system', 16))
        self.preco_entry = ctk.CTkEntry(self, height=30, placeholder_text='Digite o preço do produto')
        self.preco_label.grid(row=3, column=0, columnspan=2, sticky='w')
        self.preco_entry.grid(row=4, column=0, columnspan=2, sticky='new')

        self.quantidade_label = ctk.CTkLabel(self, text='Quantidade *', font=('system', 16))
        self.quantidade_entry = ctk.CTkEntry(self, height=30, placeholder_text='Digite a quantidade do produto')
        self.quantidade_label.grid(row=5, column=0, columnspan=2, sticky='w')
        self.quantidade_entry.grid(row=6, column=0, columnspan=2, sticky='new')

        self.unidade_label = ctk.CTkLabel(self, text='Unidade *', font=('system', 16))
        self.unidade_combobox = ctk.CTkComboBox(self, values=[unidade.name for unidade in UnidadeProduto], height=30)
        self.unidade_label.grid(row=7, column=0, columnspan=2, sticky='w')
        self.unidade_combobox.grid(row=8, column=0, columnspan=2, sticky='new')

        self.botao_cadastrar = ViewUtils.obter_botao(self, 'Cadastrar Produto')
        self.botao_cadastrar.configure(command=self.cadastrar_produto)
        self.botao_cadastrar.grid(row=9, column=0, columnspan=2, pady=(20, 0))

    def cadastrar_produto(self):
        nome = self.nome_entry.get().lower()  # Converte o nome para minúsculas
        preco = float(self.preco_entry.get())
        quantidade = float(self.quantidade_entry.get())
        unidade = self.unidade_combobox.get()
        feirante = self.controller_main.usuario_logado.to_dict()
        
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
        
        self.controller_main.controller_produto.salvar_produto(dados)
        ViewUtils.abrir_popup_mensagem('Produto salvo com sucesso!', 'green')