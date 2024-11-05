from datetime import datetime, timedelta
from dao.dao_reserva import DaoReserva
from model.cesta import Cesta
from model.cliente import Cliente
from model.dia_funcionamento import DiaSemana
from model.feirante import Feirante
from model.reserva import Reserva, StatusReserva


class ControllerReserva:
    __instancia = None

    def __init__(self):
        self.__dao_reserva = DaoReserva()
        self.__map_dias = {
            DiaSemana.SEG: 0,
            DiaSemana.TER: 1,
            DiaSemana.QUA: 2,
            DiaSemana.QUI: 3,
            DiaSemana.SEX: 4,
            DiaSemana.SAB: 5,
            DiaSemana.DOM: 6,
        }

    def __new__(cls, *args):
        if ControllerReserva.__instancia is None:
            ControllerReserva.__instancia = object.__new__(cls)
        return ControllerReserva.__instancia

    def cadastrar_reserva(self, cesta: Cesta, cliente: Cliente):
        reserva = Reserva(
            cesta,
            cliente,
            StatusReserva.PENDENTE,
            datetime.now(),
            None,
            None,
            self.calcular_disponivel_ate(cesta.feirante),
        )
        self.__dao_reserva.inserir_reserva(reserva)

    def calcular_disponivel_ate(self, feirante: Feirante) -> datetime:
        dia_atual = datetime.now().weekday()
        dias_feirante = {self.__map_dias[dia.dia_semana]: dia for dia in feirante.dias_funcionamento}
        dias_mais = 0
        while True:
            dia_atual = (dia_atual + 1) % 7
            dias_mais += 1
            if dias_feirante.get(dia_atual):
                proximo_dia_semana =  dias_feirante[dia_atual]
                proximo_dia_hora = datetime.strptime(proximo_dia_semana.horario_abertura, "%H:%M")
                proximo_dia = datetime.now() + timedelta(days=dias_mais)
                proximo_dia = proximo_dia.replace(hour=proximo_dia_hora.hour, minute=proximo_dia_hora.minute, second=0, microsecond=0)
                return proximo_dia + timedelta(hours=1)
