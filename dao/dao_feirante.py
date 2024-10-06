from bson import ObjectId
from dao.dao_main import DaoMain
from model.feirante import Feirante


class DaoFeirante(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if DaoFeirante.__instancia is None:
            DaoFeirante.__instancia = object.__new__(cls)
        return DaoFeirante.__instancia

    def obter_nome_collection(self) -> str:
        return 'feirantes'

    def obter_feirante_por_email(self, email: str) -> Feirante:
        return self.find_one({'email': email})

    def inserir_feirante(self, feirante: Feirante):
        return self.insert_one(feirante.to_dict())

    def atualizar_feirante(self, feirante: Feirante):
        self.update_one({ '_id': ObjectId(feirante.id) }, feirante.to_dict())

    def excluir_feirante(self, feirante: Feirante):
        self.delete_one({ '_id': ObjectId(feirante.id) })
