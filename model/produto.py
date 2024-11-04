from enum import Enum
from model.feirante import Feirante
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class UnidadeProduto(Enum):
    UNIDADE = 'Un.'
    KG = 'Kg.'


class Produto:
    def __init__(
        self,
        _id: str,
        nome: str,
        preco: float,
        imagem: str,
        quantidade: float,
        unidade: UnidadeProduto,
        feirante: Feirante
    ):
        self.__validar_campos(nome, preco, quantidade, unidade, feirante)
        self.__id = _id
        self.__nome = nome
        self.__preco = preco
        self.__imagem = imagem
        self.__quantidade = quantidade
        self.__unidade = unidade
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
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float):
        self.__preco = preco

    @property
    def imagem(self) -> str:
        return self.__imagem

    @imagem.setter
    def imagem(self, imagem: str):
        self.__imagem = imagem

    @property
    def quantidade(self) -> float:
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, quantidade: float):
        self.__quantidade = quantidade

    @property
    def unidade(self) -> UnidadeProduto:
        return self.__unidade

    @unidade.setter
    def unidade(self, unidade: UnidadeProduto):
        self.__unidade = unidade

    @property
    def feirante(self) -> Feirante:
        return self.__feirante

    @feirante.setter
    def feirante(self, feirante: Feirante):
        self.__feirante = feirante

    def to_dict(self) -> dict:
        return {
            'nome': self.__nome,
            'preco': self.__preco,
            'imagem': self.__imagem,
            'quantidade': self.__quantidade,
            'unidade': self.__unidade.name,
            'feirante': self.__feirante.id
        }

    def __validar_campos(
        self,
        nome: str,
        preco: float,
        quantidade: float,
        unidade: UnidadeProduto,
        feirante: Feirante
    ):
        if not nome:
            raise CampoObrigatorioException('Nome')
        if not preco:
            raise CampoObrigatorioException('Preço')
        if not quantidade:
            raise CampoObrigatorioException('Quantidade')
        if not unidade:
            raise CampoObrigatorioException('Unidade')
        if not feirante:
            raise CampoObrigatorioException('Feirante')
