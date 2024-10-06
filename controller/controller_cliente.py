from dao.dao_cliente import DaoCliente
from model.localizacao import Localizacao
from model.cliente import Cliente


class ControllerCliente:
    __instancia = None

    def __init__(self):
        self.__dao_cliente = DaoCliente()

    def __new__(cls):
        if ControllerCliente.__instancia is None:
            ControllerCliente.__instancia = object.__new__(cls)
        return ControllerCliente.__instancia

    def cadastrar_cliente(self, dados):
        cliente = self.criar_cliente(dados)
        res = self.__dao_cliente.inserir_cliente(cliente)
        cliente.id = res.inserted_id
        return cliente

    def atualizar_cliente(self, id_cliente, dados):
        cliente = self.criar_cliente(dados)
        cliente.id = id_cliente
        self.__dao_cliente.atualizar_cliente(cliente)
        return cliente

    def criar_cliente(self, dados) -> Cliente:
        localizacao = Localizacao(dados['localizacao']['latitude'], dados['localizacao']['longitude'])
        
        return Cliente(
            dados['nome'],
            dados['email'],
            dados['senha'],
            localizacao,
            dados['data_nascimento']
        )

    def excluir_cliente(self, cliente: Cliente):
        self.__dao_cliente.excluir_cliente(cliente)
