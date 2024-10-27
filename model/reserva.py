from enum import Enum
from datetime import datetime
from model.cesta import Cesta
from model.cliente import Cliente
from exception.campo_obrigatorio_exception import CampoObrigatorioException


class StatusReserva(Enum):
    PENDENTE = 'Pendente'
    ENTREGUE = 'Entregue'
    CANCELADA = 'Cancelada'


class Reserva:
    def __init__(
        self,
        cesta: Cesta,
        cliente: Cliente,
        status: StatusReserva,
        data_reserva: datetime,
        data_entrega: datetime,
        data_cancelamento: datetime,
        disponivel_ate: datetime,
    ):
        self.__validar_campos(cesta, cliente, status, data_reserva, disponivel_ate)
        self.__id = None
        self.__cesta = cesta
        self.__cliente = cliente
        self.__status = status
        self.__data_reserva = data_reserva
        self.__data_entrega = data_entrega
        self.__data_cancelamento = data_cancelamento
        self.__disponivel_ate = disponivel_ate

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        if self.__id is None:
            self.__id = id

    @property
    def cesta(self) -> Cesta:
        return self.__cesta

    @cesta.setter
    def cesta(self, cesta: Cesta):
        self.__cesta = cesta

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente: Cliente):
        self.__cliente = cliente

    @property
    def status(self) -> StatusReserva:
        return self.__status

    @status.setter
    def status(self, status: StatusReserva):
        self.__status = status

    @property
    def data_reserva(self) -> datetime:
        return self.__data_reserva

    @data_reserva.setter
    def data_reserva(self, data_reserva: datetime):
        self.__data_reserva = data_reserva

    @property
    def data_entrega(self) -> datetime:
        return self.__data_entrega

    @data_entrega.setter
    def data_entrega(self, data_entrega: datetime):
        self.__data_entrega = data_entrega

    @property
    def data_cancelamento(self) -> datetime:
        return self.__data_cancelamento

    @data_cancelamento.setter
    def data_cancelamento(self, data_cancelamento: datetime):
        self.__data_cancelamento = data_cancelamento

    @property
    def disponivel_ate(self) -> datetime:
        return self.__disponivel_ate

    @disponivel_ate.setter
    def disponivel_ate(self, disponivel_ate: datetime):
        self.__disponivel_ate = disponivel_ate

    def to_dict(self) -> dict:
        return {
            'cesta': self.__cesta.id,
            'cliente': self.__cliente.id,
            'status': self.__status.name,
            'data_reserva': self.__data_reserva.isoformat(),
            'data_entrega': self.__data_entrega.isoformat(),
            'data_cancelamento': self.__data_cancelamento.isoformat(),
            'disponivel_ate': self.__disponivel_ate.isoformat(),
        }

    def __validar_campos(
        self,
        cesta: Cesta,
        cliente: Cliente,
        status: StatusReserva,
        data_reserva: datetime,
        disponivel_ate: datetime,
    ):
        if not cesta:
            raise CampoObrigatorioException('Cesta')
        if not cliente:
            raise CampoObrigatorioException('Cliente')
        if not status:
            raise CampoObrigatorioException('Status')
        if not data_reserva:
            raise CampoObrigatorioException('Data da reserva')
        if not disponivel_ate:
            raise CampoObrigatorioException('Disponível até')
