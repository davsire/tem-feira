

class CampoObrigatorioException(Exception):

    def __init__(self, campo: str):
        super().__init__(f'O campo \'{campo}\' é obrigatório!')
