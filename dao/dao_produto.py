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

    def obter_produto_por_id(self, produto_id: str):
        return self.find_one({'_id': ObjectId(produto_id)})

    def excluir_produtos_por_feirante(self, feirante_id: str):
        self.delete_many({'feirante': ObjectId(feirante_id)})

    def decrementar_quantidade_produto(self, produto_id: str, quantidade: float):
        self.update_one({'_id': ObjectId(produto_id)}, {'$inc': {'quantidade': -quantidade}})

    def obter_produtos_por_feirante(self, feirante_id: str, apenas_disponiveis: bool):
        query = {'feirante': ObjectId(feirante_id)}
        if apenas_disponiveis:
            query['quantidade'] = { '$gt': 0 }
        return self.aggregation([
            {
                '$match': query
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
