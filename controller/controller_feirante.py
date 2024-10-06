from dao.dao_feirante import DaoFeirante


class ControllerFeirante:
    __instancia = None

    def __init__(self):
        self.__dao_feirante = DaoFeirante()

    def __new__(cls):
        if ControllerFeirante.__instancia is None:
            ControllerFeirante.__instancia = object.__new__(cls)
        return ControllerFeirante.__instancia

    def cadastrar_feirante(self, dados):
        print('Cadastrando feirante')
