from functools import partial
import customtkinter as ctk
from PIL import Image
from tktooltip import ToolTip
from model.cesta import Cesta
from model.feirante import Feirante
from model.produto import Produto
from model.usuario import TipoUsuario
from view.view_utils import ViewUtils


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


class FrameCestas(ctk.CTkScrollableFrame):
    def __init__(self, master, cestas: list[Cesta], frame_detalhes):
        super().__init__(master)
        self.configure(fg_color='white')
        self.cestas_map = {}

        if len(cestas) == 0:
            label_sem_cestas = ctk.CTkLabel(self,
                                            text='O feirante ainda não cadastrou cestas disponíveis...',
                                            font=('system', 22, 'bold'))
            label_sem_cestas.pack(pady=20, anchor='center')
            return

        for idx, cesta in enumerate(cestas):
            cesta_elm = ctk.CTkFrame(self, fg_color='white', border_width=2, border_color='black', corner_radius=5)

            nome_cesta = ctk.CTkLabel(cesta_elm, text=cesta.nome, width=500, font=('system', 20, 'bold'))
            nome_cesta.grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=10)
            ToolTip(nome_cesta, f'{cesta.nome} - R${cesta.preco_total}', bg='black', fg='white')

            imagem_cesta = ctk.CTkImage(light_image=Image.open('./assets/img/cesta.jpg'), size=(180, 140))
            imagem_cesta_lbl = ctk.CTkLabel(cesta_elm, image=imagem_cesta, text='')
            imagem_cesta_lbl.grid(row=1, column=0, padx=10)

            produtos_frame = ctk.CTkFrame(cesta_elm, fg_color='white')
            produtos_frame.grid(row=1, column=1, sticky='w')
            for idx_p, produto in enumerate(cesta.produtos):
                produto = ctk.CTkLabel(produtos_frame,
                                       text=f'{produto.quantidade} {produto.produto.unidade.value} {produto.produto.nome}',
                                       font=('system', 16))
                produto.grid(row=idx_p, column=0, pady=5, sticky='w')

            preco_cesta = ctk.CTkLabel(cesta_elm, text=f'R${cesta.preco_total}', font=('system', 18))
            preco_cesta.grid(row=2, column=0, columnspan=2, pady=(10, 5), padx=10)

            cesta_elm.grid(row=idx, column=0, padx=15, pady=(0, 30), sticky='nswe')
            self.cestas_map[cesta.id] = cesta_elm

            if frame_detalhes.controller_main.tipo_usuario_logado == TipoUsuario.CLIENTE:
                botao_reservar = ViewUtils.obter_botao(self, 'Reservar')
                botao_reservar.grid(row=idx, column=1)
                acao_reserva = partial(frame_detalhes.reservar_cesta, cesta)
                botao_reservar.configure(command=acao_reserva)
            else:
                botao_excluir = ViewUtils.obter_botao(self, 'Excluir', '#bf1900')
                botao_excluir.grid(row=idx, column=1)
                #acao_excluir = partial(frame_detalhes.reservar_cesta, cesta)
                #botao_excluir.configure(command=acao_excluir)


class FrameDetalhesFeirante(ctk.CTkFrame):
    def __init__(self, master, controller_main, feirante: Feirante):
        super().__init__(master)
        self.controller_main = controller_main
        self.__feirante = feirante
        self.configure(fg_color='white')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1, weight=1)

        self.produtos = controller_main.obter_produtos_por_feirante(feirante.id)
        self.cestas = controller_main.obter_cestas_por_feirante(feirante.id)

        self.informacoes = FrameInformacoes(self, feirante)
        self.informacoes.grid(row=0, column=0, sticky='nsew')

        self.tabview = ctk.CTkTabview(
            self,
            fg_color='white',
            segmented_button_fg_color='white',
            segmented_button_selected_color='#00bf63',
            text_color='white',
        )
        self.tabview.grid(row=1, column=0, sticky='nsew')
        self.tabview._segmented_button.configure(font=('system', 22, 'bold'), corner_radius=20)
        self.tabview.add('Produtos')
        self.tabview.add('Cestas')

        self.frame_produtos = FrameProdutos(self.tabview.tab('Produtos'), self.produtos)
        self.frame_cestas = FrameCestas(self.tabview.tab('Cestas'), self.cestas, self)
        self.frame_produtos.pack(fill="both", expand=True)
        self.frame_cestas.pack(fill="both", expand=True)

    def reservar_cesta(self, cesta: Cesta):
        self.controller_main.confirmar_reserva_cesta(cesta, self.recarregar_produtos_cestas)

    def recarregar_produtos_cestas(self):
        self.produtos = self.controller_main.obter_produtos_por_feirante(self.__feirante.id)
        self.cestas = self.controller_main.obter_cestas_por_feirante(self.__feirante.id)
        self.frame_produtos.pack_forget()
        self.frame_cestas.pack_forget()
        self.frame_produtos = FrameProdutos(self.tabview.tab('Produtos'), self.produtos)
        self.frame_cestas = FrameCestas(self.tabview.tab('Cestas'), self.cestas, self)
        self.frame_produtos.pack(fill="both", expand=True)
        self.frame_cestas.pack(fill="both", expand=True)
