from abc import ABC
from localizacao import Localizacao


class Usuario(ABC):

    def __init__(self, email: str, senha: str, localizacao: Localizacao):
        self.__id = None
        self.__email = email
        self.__senha = senha
        self.__localizacao = localizacao

    @property
    def id(self):
        return self.__id

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    @property
    def senha(self) -> str:
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        self.__senha = senha

    @property
    def localizacao(self) -> Localizacao:
        return self.__localizacao

    @localizacao.setter
    def localizacao(self, localizacao: Localizacao):
        self.__localizacao = localizacao
