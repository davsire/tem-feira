from datetime import time
from enum import Enum


class DiaSemana(Enum):
    DOM = 'DOMINGO',
    SEG = 'SEGUNDA',
    TER = 'TERCA',
    QUA = 'QUARTA',
    QUI = 'QUINTA',
    SEX = 'SEXTA',
    SAB = 'SABADO'


class DiaFuncionamento:

    def __init__(self, dia_semana: DiaSemana, horario_abertura: time, horario_fechamento: time):
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
    def horario_abertura(self) -> time:
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, horario_abertura: time):
        self.__horario_abertura = horario_abertura

    @property
    def horario_fechamento(self) -> time:
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, horario_fechamento: time):
        self.__horario_fechamento = horario_fechamento
