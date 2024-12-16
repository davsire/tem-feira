from controller.controller_cesta import ControllerCesta
from controller.controller_cliente import ControllerCliente
from controller.controller_feirante import ControllerFeirante
from controller.controller_produto import ControllerProduto
from controller.controller_reserva import ControllerReserva
from model.cesta import Cesta
from model.cliente import Cliente
from model.feirante import Feirante
from model.produto import Produto
from model.usuario import TipoUsuario
from view.view_main import ViewMain
from view.view_utils import ViewUtils


class ControllerMain:
    __instancia = None

    def __init__(self):
        self.__usuario_logado: Feirante | Cliente | None = None
        self.__tipo_usuario_logado: TipoUsuario | None = None
        self.__controller_cesta = ControllerCesta(self)
        self.__controller_cliente = ControllerCliente(self)
        self.__controller_feirante = ControllerFeirante(self)
        self.__controller_produto = ControllerProduto(self)
        self.__controller_reserva = ControllerReserva()
        self.__app = ViewMain(self)

    def __new__(cls):
        if ControllerMain.__instancia is None:
            ControllerMain.__instancia = object.__new__(cls)
        return ControllerMain.__instancia

    @property
    def usuario_logado(self) -> Feirante | Cliente:
        return self.__usuario_logado

    @property
    def tipo_usuario_logado(self) -> TipoUsuario:
        return self.__tipo_usuario_logado

    @property
    def controller_feirante(self) -> ControllerFeirante:
        return self.__controller_feirante

    @property
    def controller_produto(self) -> ControllerProduto:
        return self.__controller_produto

    @property
    def controller_cesta(self) -> ControllerCesta:
        return self.__controller_cesta

    @property
    def controller_reserva(self) -> ControllerReserva:
        return self.__controller_reserva

    def iniciar_app(self):
        self.__app.mainloop()

    def cadastrar_usuario(self, dados, tipo: TipoUsuario):
        if dados['email'] and self.__validar_email_existente(dados['email']):
            ViewUtils.abrir_popup_mensagem('E-mail já cadastrado no sistema!', '#bf1900')
            return
        try:
            usuario = None
            if tipo == TipoUsuario.FEIRANTE:
                usuario = self.__controller_feirante.cadastrar_feirante(dados)
            if tipo == TipoUsuario.CLIENTE:
                usuario = self.__controller_cliente.cadastrar_cliente(dados)
            if usuario:
                self.__usuario_logado = usuario
                self.__tipo_usuario_logado = tipo
                self.__app.alternar_telas('base')
        except Exception as e:
            ViewUtils.abrir_popup_mensagem(str(e), '#bf1900')

    def logar_usuario(self, dados):
        try:
            feirante = self.__controller_feirante.logar_feirante(dados)
            cliente = self.__controller_cliente.logar_cliente(dados)
            if feirante or cliente:
                self.__usuario_logado = feirante or cliente
                self.__tipo_usuario_logado = TipoUsuario.FEIRANTE if feirante else TipoUsuario.CLIENTE
                self.__app.alternar_telas('base')
                return
            ViewUtils.abrir_popup_mensagem('E-mail ou senha incorretos!', '#bf1900')
        except Exception as e:
            ViewUtils.abrir_popup_mensagem(str(e), '#bf1900')

    def logout(self):
        self.__usuario_logado = None
        self.__tipo_usuario_logado = None
        self.__app.alternar_telas('login_cadastro')

    def atualizar_usuario(self, dados):
        try:
            if self.__tipo_usuario_logado == TipoUsuario.FEIRANTE:
                self.__usuario_logado = self.__controller_feirante.atualizar_feirante(self.__usuario_logado.id, dados)
            if self.__tipo_usuario_logado == TipoUsuario.CLIENTE:
                self.__usuario_logado = self.__controller_cliente.atualizar_cliente(self.__usuario_logado.id, dados)
            ViewUtils.abrir_popup_mensagem('Dados atualizados com sucesso!', 'green')
        except Exception as e:
            ViewUtils.abrir_popup_mensagem(str(e), '#bf1900')

    def confirmar_exclusao_conta(self):
        ViewUtils.abrir_popup_confirmacao(
            'Tem certeza que deseja excluir sua conta?',
            'Excluir',
            self.excluir_conta,
            '#bf1900'
        )

    def excluir_conta(self):
        if self.__tipo_usuario_logado == TipoUsuario.FEIRANTE:
            self.__controller_feirante.excluir_feirante(self.__usuario_logado)
        if self.__tipo_usuario_logado == TipoUsuario.CLIENTE:
            self.__controller_cliente.excluir_cliente(self.__usuario_logado)
        self.logout()
        ViewUtils.abrir_popup_mensagem('Conta excluída com sucesso!', 'green')

    def obter_localizacao_usuario_logado(self):
        if self.__usuario_logado and hasattr(self.__usuario_logado, 'localizacao'):
            localizacao = self.__usuario_logado.localizacao
            return localizacao.latitude, localizacao.longitude
        return None

    def obter_feirantes(self) -> list[Feirante]:
        return self.__controller_feirante.obter_feirantes()

    def obter_feirante_por_nome(self, nome: str) -> Feirante | None:
        return self.__controller_feirante.obter_feirante_por_nome(nome)

    def obter_produtos_por_feirante(self, feirante_id: str) -> list[Produto]:
        return self.__controller_produto.obter_produtos_por_feirante(feirante_id, self.tipo_usuario_logado == TipoUsuario.CLIENTE)

    def obter_cestas_por_feirante(self, feirante_id: str) -> list[Cesta]:
        return self.__controller_cesta.obter_cestas_por_feirante(feirante_id)

    def confirmar_reserva_cesta(self, cesta: Cesta, callback_reserva):
        ViewUtils.abrir_popup_confirmacao(
            f'Reservar "{cesta.nome}"?',
            'Reservar',
            lambda: (self.reservar_cesta(cesta), callback_reserva()),
        )

    def reservar_cesta(self, cesta: Cesta):
        if self.__controller_cesta.verificar_cesta_reservada(cesta.id):
            ViewUtils.abrir_popup_mensagem('A cesta já está reservada...')
            return
        if self.__controller_produto.verificar_produtos_cesta_indisponiveis(cesta.produtos):
            ViewUtils.abrir_popup_mensagem('Um ou mais produtos da cesta não estão disponíveis na quantidade desejada...')
            return
        self.__controller_reserva.cadastrar_reserva(cesta, self.__usuario_logado)
        self.__controller_cesta.marcar_cesta_reservada(cesta.id, True)
        for produto in cesta.produtos:
            self.__controller_produto.decrementar_quantidade_produto(produto.produto.id, produto.quantidade)
        ViewUtils.abrir_popup_mensagem('Cesta reservada!')
    
    def confirmar_criar_cesta_pronta(self, produtos_selecionados, produtos_map, callback_criacao):
        if self.valida_criacao_cesta(produtos_selecionados, produtos_map) and self.valida_quantidades(produtos_selecionados):
            ViewUtils.abrir_popup_input(
                f'Informe o nome da cesta:',
                'Criar',
                lambda nome_cesta: (self.criar_cesta_pronta(nome_cesta, produtos_selecionados), callback_criacao()),
                "O nome da cesta não pode ser vazio!"
            )

    def criar_cesta_pronta(self, nome_cesta, produtos_selecionados):

        produtos_id = {}
        for produto_id, produto_data in produtos_selecionados.items():
            produtos_id[produto_id] = produto_data['quantidade']

        lista_produtos = list(produtos_selecionados.values())

        dados = {
            'nome': nome_cesta,
            'produtos': lista_produtos,
            'preco_total': self.calcular_preco(lista_produtos),
            'personalizada': False,
            'reservada': False,
            'produtos_id': produtos_id,
            'feirante_id': self.__usuario_logado.id
        }

        self.__controller_cesta.cadastrar_cesta_pronta(dados)
        ViewUtils.abrir_popup_mensagem('Cesta criada com sucesso!')

    def calcular_preco(self, lista_produtos) -> float:
        preco_total = 0
        for produto in lista_produtos:
            preco_total += produto['produto'].preco * produto['quantidade']

        return round(preco_total, 2)

    def valida_criacao_cesta(self, produtos_selecionados, produtos_map):
        if not(produtos_selecionados):
            ViewUtils.abrir_popup_mensagem("Não é possivel criar uma cesta vazia.", cor_mensagem='red')
            return
        
        mapa_produtos = produtos_map.items()

        for produto_id, produto_data in mapa_produtos:
            entrada_quantidade = produto_data["quantidade"]
            if entrada_quantidade:
                quantidade = entrada_quantidade.get().strip()
                if produto_id in produtos_selecionados:
                    try:
                        quantidade = float(quantidade)
                    except:
                        ViewUtils.abrir_popup_mensagem("Informe a quantidade do produto", cor_mensagem='red')
                        return
                    if quantidade <= 0:
                        ViewUtils.abrir_popup_mensagem("Insira uma quantidade válida", cor_mensagem='red')
                        return
                    produtos_selecionados[produto_id]["quantidade"] = quantidade
        return True

    def valida_quantidades(self, produtos_selecionados):
        mapa_selecionados = produtos_selecionados.items()

        try:
            for produto_id, produto_data in mapa_selecionados:
                input_quantidade = produto_data["quantidade"]
                quantidade_produto = produto_data["produto"].quantidade
                if input_quantidade > quantidade_produto:
                    raise ValueError("A quantidade inserida é maior que a disponível")
        except ValueError as e:
            ViewUtils.abrir_popup_mensagem(e, cor_mensagem='red')
            return
        return True

    def confirmar_exclusao_cesta(self, cesta: Cesta, callback_excluir):
        ViewUtils.abrir_popup_confirmacao(
            f'Excluir "{cesta.nome}"?',
            'Excluir',
            lambda: (self.excluir_cesta(cesta), callback_excluir()),
            '#bf1900'
        )

    def excluir_cesta(self, cesta: Cesta):
        self.__controller_cesta.excluir_cesta(cesta)
        ViewUtils.abrir_popup_mensagem('Cesta excluida!')

    def abrir_tela_custom(self, tela, *args):
        if self.__usuario_logado is not None:
            self.__app.frame.abrir_tela_custom(tela, *args)

    def __validar_email_existente(self, email: str) -> bool:
        feirante = self.__controller_feirante.obter_feirante_por_email(email)
        cliente = self.__controller_cliente.obter_cliente_por_email(email)
        return bool(feirante or cliente)
