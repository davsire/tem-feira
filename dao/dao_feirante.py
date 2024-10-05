from dao.dao_main import DaoMain


class DaoFeirante(DaoMain):

    def __init__(self):
        super().__init__()

    def obter_nome_collection(self) -> str:
        return 'feirantes'
