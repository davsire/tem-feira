from enum import Enum
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class DiaSemana(Enum):
    DOM = 'Domingo'
    SEG = 'Segunda'
    TER = 'Terça'
    QUA = 'Quarta'
    QUI = 'Quinta'
    SEX = 'Sexta'
    SAB = 'Sábado'


class DiaFuncionamento:

    def __init__(self, dia_semana: DiaSemana, horario_abertura: str, horario_fechamento: str):
        self.__validar_campos(dia_semana, horario_abertura, horario_fechamento)
        self.__dia_semana = dia_semana
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento

    @property
    def dia_semana(self) -> DiaSemana:
        return self.__dia_semana

    @dia_semana.setter
    def dia_semana(self, dia_semana: DiaSemana):
        self.__dia_semana = dia_semana

    @property
    def horario_abertura(self) -> str:
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, horario_abertura: str):
        self.__horario_abertura = horario_abertura

    @property
    def horario_fechamento(self) -> str:
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, horario_fechamento: str):
        self.__horario_fechamento = horario_fechamento

    def to_dict(self):
        return {
            'dia_semana': self.dia_semana.name,
            'horario_abertura': self.horario_abertura,
            'horario_fechamento': self.horario_fechamento,
        }

    def __validar_campos(self, dia_semana: DiaSemana, horario_abertura: str, horario_fechamento: str):
        if not dia_semana:
            raise CampoObrigatorioException('Dia da semana')
        if not horario_abertura:
            raise CampoObrigatorioException('Horário de abertura')
        if not horario_fechamento:
            raise CampoObrigatorioException('Horário de fechamento')
