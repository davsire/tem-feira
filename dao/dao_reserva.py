from bson import ObjectId
from dao.dao_main import DaoMain
from model.reserva import Reserva


class DaoReserva(DaoMain):
    __instancia = None

    def __init__(self):
        super().__init__()

    def __new__(cls):
        if DaoReserva.__instancia is None:
            DaoReserva.__instancia = object.__new__(cls)
        return DaoReserva.__instancia

    def obter_nome_collection(self) -> str:
        return 'reservas'

    def inserir_reserva(self, reserva: Reserva):
        return self.insert_one(reserva.to_dict())

    def excluir_reservas_por_cliente(self, cliente_id: str):
        self.delete_many({'cliente': ObjectId(cliente_id)})

    def excluir_reserva_por_cesta(self, cesta_id: str):
        self.delete_one({'cesta': ObjectId(cesta_id)})
