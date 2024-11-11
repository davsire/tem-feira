from model.feirante import Feirante
from model.produto_cesta import ProdutoCesta
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class Cesta:
    def __init__(
        self,
        _id: str,
        nome: str,
        produtos: list[ProdutoCesta],
        preco_total: float,
        personalizada: bool,
        reservada: bool,
        feirante: Feirante
    ):
        self.__validar_campos(nome, produtos, preco_total, personalizada, reservada, feirante)
        self.__id = _id
        self.__nome = nome
        self.__produtos = produtos
        self.__preco_total = preco_total
        self.__personalizada = personalizada
        self.__reservada = reservada
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

    @property
    def reservada(self) -> bool:
        return self.__reservada

    @reservada.setter
    def reservada(self, reservada: bool):
        self.__reservada = reservada

    @property
    def feirante(self) -> Feirante:
        return self.__feirante

    @feirante.setter
    def feirante(self, feirante: Feirante):
        self.__feirante = feirante

    def to_dict(self) -> dict:
        return {
            'nome': self.__nome,
            'produtos': [produto.to_dict() for produto in self.__produtos],
            'preco_total': self.__preco_total,
            'personalizada': self.__personalizada,
            'feirante': self.__feirante.id
        }

    def to_dict_pronto(self) -> dict:
        return {
            'nome': self.__nome,
            'produtos': [produto.to_dict_pronto() for produto in self.__produtos],
            'preco_total': self.__preco_total,
            'personalizada': self.__personalizada,
            'feirante': self.__feirante,
            'reservada' : False
        }

    def __validar_campos(
        self,
        nome: str,
        produtos: list[ProdutoCesta],
        preco_total: float,
        personalizada: bool,
        reservada: bool,
        feirante: Feirante
    ):
        if not nome:
            raise CampoObrigatorioException('Nome')
        if produtos is None:
            raise CampoObrigatorioException('Produtos')
        if not preco_total:
            raise CampoObrigatorioException('Preço total')
        if personalizada is None:
            raise CampoObrigatorioException('Personalizada')
        if reservada is None:
            raise CampoObrigatorioException('Reservada')
        if not feirante:
            raise CampoObrigatorioException('Feirante')
