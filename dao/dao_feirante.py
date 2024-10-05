from bson import ObjectId
from dao.dao_main import DaoMain
from model.feirante import Feirante


class DaoFeirante(DaoMain):

    def __init__(self):
        super().__init__()

    def obter_nome_collection(self) -> str:
        return 'feirantes'

    def obter_feirante_por_email_senha(self, email: str, senha: str) -> Feirante:
        return self.find_one({'email': email, 'senha': senha})

    def inserir_feirante(self, feirante: Feirante):
        self.insert_one(feirante.to_dict())

    def atualizar_feirante(self, feirante: Feirante):
        self.update_one({ '_id': ObjectId(feirante.id) }, feirante.to_dict())

    def remover_feirante(self, feirante: Feirante):
        self.delete_one({ '_id': ObjectId(feirante.id) })
