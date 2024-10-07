from abc import ABC
from enum import Enum
from model.localizacao import Localizacao


class TipoUsuario(Enum):
    FEIRANTE = 'Feirante'
    CLIENTE = 'Cliente'


class Usuario(ABC):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def __init__(self, email: str, senha: bytes, localizacao: Localizacao):
        self.__id = None
        self.__email = email
        self.__senha = senha
        self.__localizacao = localizacao

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        if self.__id is None:
            self.__id = id

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email

    @property
    def senha(self) -> bytes:
        return self.__senha

    @senha.setter
    def senha(self, senha: bytes):
        self.__senha = senha

    @property
    def localizacao(self) -> Localizacao:
        return self.__localizacao

    @localizacao.setter
    def localizacao(self, localizacao: Localizacao):
        self.__localizacao = localizacao
