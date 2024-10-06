import re
from enum import Enum
from exception.campo_obrigatorio_exception import CampoObrigatorioException
from model.usuario import Usuario
from model.localizacao import Localizacao
from model.dia_funcionamento import DiaFuncionamento


class FormaContato(Enum):
    WHATSAPP = 'WHATSAPP'
    INSTAGRAM = 'INSTAGRAM'
    FACEBOOK = 'FACEBOOK'


class Feirante(Usuario):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

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
        self.__validar_campos(email, senha, localizacao, nome_feira, forma_contato, contato, dias_funcionamento)
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

    def to_dict(self):
        return  {
            'email': self.email,
            'senha': self.senha,
            'nome_feira': self.nome_feira,
            'forma_contato': self.forma_contato.name,
            'contato': self.contato,
            'localizacao': self.localizacao.to_dict(),
            'dias_funcionamento': [dia.to_dict() for dia in self.dias_funcionamento],
        }

    def __validar_campos(self,
            email: str,
            senha: str,
            localizacao: Localizacao,
            nome_feira: str,
            forma_contato: FormaContato,
            contato: str,
            dias_funcionamento: list[DiaFuncionamento]
    ):
        if not nome_feira:
            raise CampoObrigatorioException('Nome da feira')
        if not forma_contato or not contato:
            raise CampoObrigatorioException('Contato')
        if not localizacao:
            raise CampoObrigatorioException('Localização')
        if not email:
            raise CampoObrigatorioException('E-mail')
        if not re.match(Feirante.email_regex, email):
            raise Exception('Informe um e-mail válido!')
        if not senha:
            raise CampoObrigatorioException('Senha')
        if not dias_funcionamento:
            raise CampoObrigatorioException('Dias de funcionamento')
