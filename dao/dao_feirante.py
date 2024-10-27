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

    def obter_feirante_por_email(self, email: str) -> dict:
        return self.find_one({'email': email})

    def inserir_feirante(self, feirante: Feirante):
        return self.insert_one(feirante.to_dict())

    def atualizar_feirante(self, feirante: Feirante):
        self.update_one({ '_id': ObjectId(feirante.id) }, feirante.to_dict())

    def excluir_feirante(self, feirante: Feirante):
        self.delete_one({ '_id': ObjectId(feirante.id) })

    def obter_localizacoes_feirantes(self):
        feirantes = self.find({})
        localizacoes = []
        for feirante in feirantes:
            nome_feira = feirante.get('nome_feira')
            latitude = feirante.get('localizacao', {}).get('latitude')
            longitude = feirante.get('localizacao', {}).get('longitude')
            if nome_feira and latitude is not None and longitude is not None:
                localizacoes.append((nome_feira, latitude, longitude))
        return localizacoes
