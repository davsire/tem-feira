from bson import ObjectId
from dao.dao_main import DaoMain
from model.produto import Produto


class DaoProduto(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()
        self.collection = self.db[self.obter_nome_collection()]

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
        
    def buscar_produto_por_nome(self, nome: str):
        return self.collection.find_one({'nome': nome})

    def salvar_produto(self, produto: Produto):
        # Converta o objeto Produto para um dicionário
        produto_dict = {
            '_id': ObjectId(produto.id) if produto.id else ObjectId(),
            'nome': produto.nome,
            'preco': produto.preco,
            'imagem': produto.imagem,
            'quantidade': produto.quantidade,
            'unidade': produto.unidade.value,
            'feirante': ObjectId(produto.feirante.id),  # Supondo que feirante tenha um atributo id
        }
        
        # Verifique se um produto com o mesmo nome já existe no banco de dados
        produto_existente = self.buscar_produto_por_nome(produto.nome)
        
        if produto_existente:
            # Atualize o documento existente
            self.collection.update_one({'_id': produto_existente['_id']}, {'$set': produto_dict})
            print('Produto atualizado no banco de dados!')
        else:
            # Insira um novo documento
            self.collection.insert_one(produto_dict)
            print('Produto salvo no banco de dados!')