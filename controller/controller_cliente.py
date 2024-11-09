import bcrypt
from dao.dao_cliente import DaoCliente
from model.localizacao import Localizacao
from model.cliente import Cliente


class ControllerCliente:
    __instancia = None

    def __init__(self, controller_main):
        self.__dao_cliente = DaoCliente()
        self.__controller_main = controller_main

    def __new__(cls, *args):
        if ControllerCliente.__instancia is None:
            ControllerCliente.__instancia = object.__new__(cls)
        return ControllerCliente.__instancia

    def cadastrar_cliente(self, dados) -> Cliente:
        cliente = self.criar_cliente(dados)
        cliente.senha = bcrypt.hashpw(bytes(dados["senha"], 'utf-8'), bcrypt.gensalt())
        res = self.__dao_cliente.inserir_cliente(cliente)
        cliente.id = res.inserted_id
        return cliente

    def atualizar_cliente(self, id_cliente, dados) -> Cliente:
        cliente = self.criar_cliente(dados)
        cliente.senha = bcrypt.hashpw(bytes(dados["senha"], 'utf-8'), bcrypt.gensalt())
        cliente.id = id_cliente
        self.__dao_cliente.atualizar_cliente(cliente)
        return cliente

    def criar_cliente(self, dados) -> Cliente:
        localizacao = Localizacao(dados['localizacao']['latitude'], dados['localizacao']['longitude'])
        return Cliente(
            dados.get('_id'),
            dados['email'],
            dados['senha'],
            localizacao,
            dados['nome'],
            dados['data_nascimento']
        )

    def logar_cliente(self, dados) -> Cliente | None:
        cliente_mongo = self.__dao_cliente.obter_cliente_por_email(dados["email"])
        if cliente_mongo is None:
            return None
        if bcrypt.checkpw(bytes(dados["senha"], 'utf-8'), cliente_mongo["senha"]):
            cliente = self.criar_cliente(cliente_mongo)
            return cliente

    def obter_cliente_por_email(self, email: str) -> Cliente | None:
        cliente_mongo = self.__dao_cliente.obter_cliente_por_email(email)
        if cliente_mongo is None:
            return None
        return self.criar_cliente(cliente_mongo)

    def excluir_cliente(self, cliente: Cliente):
        self.__dao_cliente.excluir_cliente(cliente)
        self.__controller_main.controller_reserva.excluir_reservas_por_cliente(cliente.id)
