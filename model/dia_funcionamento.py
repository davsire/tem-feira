from enum import Enum


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
