from bson import ObjectId
from dao.dao_main import DaoMain
from model.produto import Produto


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

    def inserir_produto(self, produto: Produto):
        produto_dict = {
            '_id': ObjectId(produto.id) if produto.id else ObjectId(),
            'nome': produto.nome,
            'preco': produto.preco,
            'imagem': produto.imagem,
            'quantidade': produto.quantidade,
            'unidade': produto.unidade.name,
            'feirante': ObjectId(produto.feirante.id),
        }
        # Verifique se um produto com o mesmo nome já existe no banco de dados
        produto_existente = self.find_one({'nome': produto.nome.lower()})
        
        if produto_existente:
            # Remova o campo '_id' do dicionário do produto existente
            produto_dict.pop('_id', None)
            # Atualize o documento existente
            self.update_one({'_id': produto_existente['_id']}, {'$set': produto_dict})
            print('Produto atualizado no banco de dados!')
        else:
            # Insira um novo documento
            self.insert_one(produto_dict)
            # print('Novo produto inserido no banco de dados!')
            
        def excluir_produto(self, produto_id: str):
            """Exclui um produto do banco de dados"""
            self.__dao_produto.delete_one({'_id': ObjectId(produto_id)})