from dao.dao_feirante import DaoFeirante
from dao.dao_cliente import DaoCliente


class ControllerMapa:
    def __init__(self):
        self.__dao_feirante = DaoFeirante()
        self.__dao_cliente = DaoCliente()

        
    def obter_localizacoes_feirantes(self):
        return self.__dao_feirante.buscar_latitudes_longitudes()
    
    