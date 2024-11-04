from bson import ObjectId
from dao.dao_main import DaoMain


class DaoProduto(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if DaoProduto.__instancia is None:
            DaoProduto.__instancia = object.__new__(cls)
        return DaoProduto.__instancia

    def obter_nome_collection(self) -> str:
        return 'produtos'

    def obter_produtos_por_feirante(self, feirante_id: str):
        return self.aggregation([
            {
                '$match': {'feirante': ObjectId(feirante_id), 'quantidade': { '$gt': 0 }}
            },
            {
                '$lookup': {
                    'from': 'feirantes',
                    'localField': 'feirante',
                    'foreignField': '_id',
                    'as': 'feirante'
                }
            },
            {
                '$unwind': '$feirante'
            }
        ])
