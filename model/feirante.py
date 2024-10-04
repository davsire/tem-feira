from usuario import Usuario
from enum import Enum
from localizacao import Localizacao
from dia_funcionamento import DiaFuncionamento


class FormaContato(Enum):
    INSTAGRAM = 'INSTAGRAM',
    WHATSAPP = 'WHATSAPP',
    FACEBOOK = 'FACEBOOK',


class Feirante(Usuario):

    def __init__(
            self,
            email: str,
            senha: str,
            localizacao: Localizacao,
            nome_feira: str,
            forma_contato: FormaContato,
            contato: str,
            dias_funcionamento: list[DiaFuncionamento]
    ):
        super().__init__(email, senha, localizacao)
        self.__nome_feira = nome_feira
        self.__forma_contato = forma_contato
        self.__contato = contato
        self.__dias_funcionamento = dias_funcionamento

    @property
    def nome_feira(self) -> str:
        return self.__nome_feira

    @nome_feira.setter
    def nome_feira(self, nome_feira: str):
        self.__nome_feira = nome_feira

    @property
    def forma_contato(self) -> FormaContato:
        return self.__forma_contato

    @forma_contato.setter
    def forma_contato(self, forma_contato: FormaContato):
        self.__forma_contato = forma_contato

    @property
    def contato(self) -> str:
        return self.__contato

    @contato.setter
    def contato(self, contato: str):
        self.__contato = contato

    @property
    def dias_funcionamento(self) -> list[DiaFuncionamento]:
        return self.__dias_funcionamento

    @dias_funcionamento.setter
    def dias_funcionamento(self, dias_funcionamento: list[DiaFuncionamento]):
        self.__dias_funcionamento = dias_funcionamento
