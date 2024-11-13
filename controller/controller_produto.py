from dao.dao_produto import DaoProduto
from model.produto import Produto, UnidadeProduto
from model.produto_cesta import ProdutoCesta
from bson import ObjectId



class ControllerProduto:
    __instancia = None

    def __init__(self, controller_main):
        self.__dao_produto = DaoProduto()
        self.__controller_main = controller_main

    def __new__(cls, *args):
        if ControllerProduto.__instancia is None:
            ControllerProduto.__instancia = object.__new__(cls)
        return ControllerProduto.__instancia

    def obter_produtos_por_feirante(self, feirante_id: str, apenas_disponiveis: bool) -> list[Produto]:
        produtos_mongo = self.__dao_produto.obter_produtos_por_feirante(feirante_id, apenas_disponiveis)
        return [self.criar_produto(produto) for produto in produtos_mongo]

    def excluir_produtos_por_feirante(self, feirante_id: str):
        self.__dao_produto.excluir_produtos_por_feirante(feirante_id)

    def criar_produto(self, dados: dict) -> Produto:
        imagem_padrao = '/home/ale-vasco/ale/UFSC/APS/tem-feira/assets/img/icone-produto.png'
        # print('Criando produto')
        return Produto(
            dados.get('_id'),
            dados['nome'],
            dados['preco'],
            dados.get('imagem', imagem_padrao),
            dados['quantidade'],
            UnidadeProduto[dados['unidade']],
            self.__controller_main.controller_feirante.criar_feirante(dados['feirante']),
        )

    def verificar_produtos_cesta_indisponiveis(self, produtos: list[ProdutoCesta]) -> bool:
        for produto in produtos:
            if self.__dao_produto.obter_produto_por_id(produto.produto.id).get('quantidade') < produto.quantidade:
                return True
        return False

    def decrementar_quantidade_produto(self, produto_id: str, quantidade: float):
        self.__dao_produto.decrementar_quantidade_produto(produto_id, quantidade)

    def salvar_produto(self, dados: dict):
        produto = self.criar_produto(dados)
        self.__dao_produto.inserir_produto(produto)
        print('Produto salvo no banco de dados!')
        
    def inserir_produto(self, produto: Produto):
        documento = {
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "unidade": produto.unidade.name,
            "feirante": ObjectId(produto.feirante._id)
        }
        self.__dao_produto.insert_one(documento)

    def editar_produto(self, dados):
        query = {"nome": dados['nome']}
        feirante_id = dados.get('feirante')
        update = {
            "$set": {
                "preco": dados['preco'],
                "quantidade": dados['quantidade'],
                "unidade": dados['unidade'],
                "feirante": ObjectId(feirante_id)
            }
        }
        self.__dao_produto.update_one(query, update)
        
    def obter_todos_produtos(self):
        produtos = self.__dao_produto.find({})
        return [{'nome': produto['nome']} for produto in produtos]