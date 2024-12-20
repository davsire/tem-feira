from bson import ObjectId
from dao.dao_main import DaoMain
from model.cesta import Cesta


class DaoCesta(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if DaoCesta.__instancia is None:
            DaoCesta.__instancia = object.__new__(cls)
        return DaoCesta.__instancia

    def obter_nome_collection(self) -> str:
        return 'cestas'

    def obter_cesta_por_id(self, cesta_id: str) -> dict:
        return self.find_one({'_id': ObjectId(cesta_id)})

    def excluir_cesta(self, cesta: Cesta):
        self.delete_one({ '_id': ObjectId(cesta.id) })

    def excluir_cestas_por_feirante(self, feirante_id: str):
        self.delete_many({'feirante': ObjectId(feirante_id)})

    def marcar_cesta_reservada(self, cesta_id: str, reservada: bool):
        self.update_one({'_id': ObjectId(cesta_id)}, {'$set': {'reservada': reservada}})

    def inserir_cesta(self, cesta: Cesta):
        return self.insert_one(cesta.to_dict_pronto())

    def obter_cestas_por_feirante(self, feirante_id: str):
        return self.aggregation([
            {
                '$match': {'feirante': ObjectId(feirante_id), 'personalizada': False, 'reservada': False}
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
            },
            {
                '$unwind': '$produtos'
            },
            {
                '$lookup': {
                    'from': 'produtos',
                    'localField': 'produtos.produto',
                    'foreignField': '_id',
                    'as': 'produtos.produto',
                    'pipeline': [
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
                    ]
                }
            },
            {
                '$unwind': '$produtos.produto'
            },
            {
                '$group': {
                    '_id': '$_id',
                    'nome': { '$first': '$nome'},
                    'preco_total': { '$first': '$preco_total'},
                    'personalizada': { '$first': '$personalizada'},
                    'reservada': { '$first': '$reservada'},
                    'feirante': { '$first': '$feirante'},
                    'produtos': {
                        '$push': '$produtos'
                    }
                }
            }
        ])
