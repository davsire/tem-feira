from model.produto import Produto
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class ProdutoCesta:
    def __init__(self, produto: Produto, quantidade: float):
        self.__validar_campos(produto, quantidade)
        self.__produto = produto
        self.__quantidade = quantidade

    @property
    def produto(self) -> Produto:
        return self.__produto

    @produto.setter
    def produto(self, produto: Produto):
        self.__produto = produto

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: float):
        self.__quantidade = quantidade

    def to_dict(self) -> dict:
        return {
            'produto': self.__produto.id,
            'quantidade': self.__quantidade
        }

    def __validar_campos(self, produto: Produto, quantidade: float):
        if not produto:
            raise CampoObrigatorioException('Produto')
        if not quantidade:
            raise CampoObrigatorioException('Quantidade')
