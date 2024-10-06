from exception.campo_obrigatorio_exception import CampoObrigatorioException
from model.usuario import Usuario
from enum import Enum
from model.localizacao import Localizacao

class FormaContato(Enum):
    WHATSAPP = 'WHATSAPP'
    INSTAGRAM = 'INSTAGRAM'
    FACEBOOK = 'FACEBOOK'

class Cliente(Usuario):

    def __init__(
            self,
            email: str,
            senha: str,
            data_nascimento: str,
            localizacao: Localizacao,
            nome: str,
    ):
        super().__init__(email, senha, localizacao)
        self.__validar_campos(email, senha, localizacao, nome, data_nascimento)
        self.__nome = nome
        self.__data_nascimento = data_nascimento

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def data_nascimento(self) -> str:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: str):
        self.__data_nascimento = data_nascimento

    def to_dict(self):
        return {
            'email': self.email,
            'senha': self.senha,
            'nome': self.nome,
            'localizacao': self.localizacao.to_dict(),
            'data_nascimento': self.data_nascimento
        }

    def __validar_campos(self,
            email: str,
            senha: str,
            localizacao: Localizacao,
            nome: str,
            data_nascimento: str
    ):
        if not nome:
            raise CampoObrigatorioException('Nome')
        if not localizacao:
            raise CampoObrigatorioException('Localização')
        if not email:
            raise CampoObrigatorioException('E-mail')
        if not senha:
            raise CampoObrigatorioException('Senha')
        if not data_nascimento:
            raise CampoObrigatorioException('Data de Nascimento')
