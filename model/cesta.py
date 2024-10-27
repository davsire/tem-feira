from model.feirante import Feirante
from model.produto_cesta import ProdutoCesta
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class Cesta:
    def __init__(
        self,
        nome: str,
        produtos: list[ProdutoCesta],
        preco_total: float,
        personalizada: bool,
        feirante: Feirante
    ):
        self.__validar_campos(nome, produtos, preco_total, personalizada, feirante)
        self.__id = None
        self.__nome = nome
        self.__produtos = produtos
        self.__preco_total = preco_total
        self.__personalizada = personalizada
        self.__feirante = feirante

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        if self.__id is None:
            self.__id = id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def produtos(self) -> list[ProdutoCesta]:
        return self.__produtos

    @produtos.setter
    def produtos(self, produtos: list[ProdutoCesta]):
        self.__produtos = produtos

    @property
    def preco_total(self) -> float:
        return self.__preco_total

    @preco_total.setter
    def preco_total(self, preco_total: float):
        self.__preco_total = preco_total

    @property
    def personalizada(self) -> bool:
        return self.__personalizada

    @personalizada.setter
    def personalizada(self, personalizada: bool):
        self.__personalizada = personalizada

    def to_dict(self) -> dict:
        return {
            'nome': self.__nome,
            'produtos': [produto.to_dict() for produto in self.__produtos],
            'preco_total': self.__preco_total,
            'personalizada': self.__personalizada,
            'feirante': self.__feirante.id
        }

    def __validar_campos(
        self,
        nome: str,
        produtos: list[ProdutoCesta],
        preco_total: float,
        personalizada: bool,
        feirante: Feirante
    ):
        if not nome:
            raise CampoObrigatorioException('Nome')
        if not produtos:
            raise CampoObrigatorioException('Produtos')
        if not preco_total:
            raise CampoObrigatorioException('Preço total')
        if not personalizada:
            raise CampoObrigatorioException('Personalizada')
        if not feirante:
            raise CampoObrigatorioException('Feirante')
