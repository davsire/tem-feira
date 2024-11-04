from dao.dao_produto import DaoProduto
from model.produto import Produto, UnidadeProduto


class ControllerProduto:
    __instancia = None

    def __init__(self, controller_main):
        self.__dao_produto = DaoProduto()
        self.__controller_main = controller_main

    def __new__(cls, *args):
        if ControllerProduto.__instancia is None:
            ControllerProduto.__instancia = object.__new__(cls)
        return ControllerProduto.__instancia

    def obter_produtos_por_feirante(self, feirante_id: str) -> list[Produto]:
        produtos_mongo = self.__dao_produto.obter_produtos_por_feirante(feirante_id)
        return [self.criar_produto(produto) for produto in produtos_mongo]

    def criar_produto(self, dados: dict) -> Produto:
        return Produto(
            dados.get('_id'),
            dados['nome'],
            dados['preco'],
            dados['imagem'],
            dados['quantidade'],
            UnidadeProduto[dados['unidade']],
            self.__controller_main.controller_feirante.criar_feirante(dados['feirante']),
        )
