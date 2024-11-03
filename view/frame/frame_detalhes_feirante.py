import customtkinter as ctk
from PIL import Image
from tktooltip import ToolTip
from model.feirante import Feirante
from model.produto import Produto


class FrameInformacoes(ctk.CTkFrame):
    def __init__(self, master, feirante: Feirante):
        super().__init__(master)
        self.configure(fg_color='#78b661', corner_radius=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        limite_texto = 40
        self.nome_feira = ctk.CTkLabel(self, text=feirante.nome_feira, text_color='black', font=('system', 20, 'bold'))
        self.nome_feira.grid(row=0, column=0, pady=(10, 2), padx=10, sticky='nsw')

        contato = feirante.contato[:limite_texto] + ('...' if len(feirante.contato) >= limite_texto else '')
        self.contato = ctk.CTkLabel(self, text=f'Contato: {contato}', text_color='black', font=('system', 16))
        self.contato.grid(row=1, column=0, pady=2, padx=10, sticky='nsw')
        ToolTip(self.contato, feirante.contato, bg='black', fg='white')

        endereco = feirante.localizacao.endereco[:limite_texto] + ('...' if len(feirante.localizacao.endereco) >= limite_texto else '')
        self.endereco = ctk.CTkLabel(self, text=f'Endereço: {endereco}', text_color='black', font=('system', 16))
        self.endereco.grid(row=2, column=0, pady=(2, 10), padx=10, sticky='nsw')
        ToolTip(self.endereco, feirante.localizacao.endereco, bg='black', fg='white')

        dias_funcionamento = [
            f'{dia.dia_semana.value} ({dia.horario_abertura} às {dia.horario_fechamento})'
            for idx, dia in enumerate(feirante.dias_funcionamento)
        ]
        for idx in range(len(dias_funcionamento)):
            if idx > 0 and idx % 3 == 0:
                dias_funcionamento[idx] = '\n' + dias_funcionamento[idx]
        dias_funcionamento = ', '.join(dias_funcionamento)
        self.dias_funcionamento_titulo = ctk.CTkLabel(self, text='Dias de funcionamento', text_color='black', font=('system', 20, 'bold'))
        self.dias_funcionamento_titulo.grid(row=0, column=1, pady=(10, 2), padx=10, sticky='nsw')
        self.dias_funcionamento = ctk.CTkLabel(self, text=dias_funcionamento, text_color='black', font=('system', 14), justify='left')
        self.dias_funcionamento.grid(row=1, rowspan=2, column=1, pady=(2, 10), padx=10, sticky='nw')


class FrameProdutos(ctk.CTkScrollableFrame):
    def __init__(self, master, produtos: list[Produto]):
        super().__init__(master)
        self.configure(fg_color='white')
        self.limite_linha = 4
        self.produtos_map = {}

        if len(produtos) == 0:
            label_sem_produtos = ctk.CTkLabel(self,
                                              text='O feirante ainda não cadastrou produtos disponíveis...',
                                              font=('system', 22, 'bold'))
            label_sem_produtos.pack(pady=20, anchor='center')
            return

        self.bind_all("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind_all("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))
        for idx, produto in enumerate(produtos):
            coluna = idx % self.limite_linha
            linha = idx // self.limite_linha

            produto_elm = ctk.CTkFrame(self, fg_color='white', border_width=2, border_color='black', corner_radius=5)

            nome = produto.nome[:15] + ('...' if len(produto.nome) >= 15 else '')
            nome_produto = ctk.CTkLabel(produto_elm, text=nome, width=180, font=('system', 20, 'bold'))
            nome_produto.pack(pady=(10, 5), padx=10)
            ToolTip(nome_produto, f'{produto.nome} - R${produto.preco} {produto.unidade.value}', bg='black', fg='white')

            src = produto.imagem if produto.imagem else './assets/img/produto_default.png'
            imagem_produto = ctk.CTkImage(light_image=Image.open(src), size=(180, 140))
            imagem_produto_lbl = ctk.CTkLabel(produto_elm, image=imagem_produto, text='')
            imagem_produto_lbl.pack(padx=10)

            preco_produto = ctk.CTkLabel(produto_elm, text=f'R${produto.preco} {produto.unidade.value}', font=('system', 18))
            preco_produto.pack(pady=(10, 5), padx=10)

            produto_elm.grid(row=linha, column=coluna, padx=15, pady=(0, 30), sticky='nswe')
            self.produtos_map[produto.id] = produto_elm


class FrameDetalhesFeirante(ctk.CTkFrame):
    def __init__(self, master, controller_main, feirante: Feirante):
        super().__init__(master)
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)

        self.produtos = controller_main.obter_produtos_por_feirante(feirante.id)
        self.cestas = controller_main.obter_cestas_por_feirante(feirante.id)

        self.informacoes = FrameInformacoes(self, feirante)
        self.informacoes.grid(row=0, column=0, sticky='nsew')

        tabview = ctk.CTkTabview(
            self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white',
        )
        tabview.grid(row=1, column=0, sticky='nsew')
        tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        tabview.add('Produtos')
        tabview.add('Cestas')

        self.frame_produtos = FrameProdutos(tabview.tab('Produtos'), self.produtos)
        self.frame_produtos.pack(fill="both", expand=True)
