from bson import ObjectId
from dao.dao_main import DaoMain
from model.cliente import Cliente


class DaoCliente(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if DaoCliente.__instancia is None:
            DaoCliente.__instancia = object.__new__(cls)
        return DaoCliente.__instancia

    def obter_nome_collection(self) -> str:
        return 'clientes'

    def obter_cliente_por_email(self, email: str) -> dict:
        return self.find_one({'email': email})

    def inserir_cliente(self, cliente: Cliente):
        return self.insert_one(cliente.to_dict())

    def atualizar_cliente(self, cliente: Cliente):
        self.update_one({ '_id': ObjectId(cliente.id) }, cliente.to_dict())

    def excluir_cliente(self, cliente: Cliente):
        self.delete_one({ '_id': ObjectId(cliente.id) })
