from dao.dao_feirante import DaoFeirante
from model.dia_funcionamento import DiaFuncionamento, DiaSemana
from model.feirante import Feirante, FormaContato
from model.localizacao import Localizacao


class ControllerFeirante:
    __instancia = None

    def __init__(self):
        self.__dao_feirante = DaoFeirante()

    def __new__(cls):
        if ControllerFeirante.__instancia is None:
            ControllerFeirante.__instancia = object.__new__(cls)
        return ControllerFeirante.__instancia

    def cadastrar_feirante(self, dados):
        feirante = self.criar_feirante(dados)
        self.__dao_feirante.inserir_feirante(feirante)
        return feirante

    def criar_feirante(self, dados) -> Feirante:
        localizacao = Localizacao(dados['localizacao']['latitude'], dados['localizacao']['longitude'])
        dias_funcionamento = [
            DiaFuncionamento(DiaSemana[dia['dia_semana']], dia['horario_abertura'], dia['horario_fechamento'])
            for dia in dados['dias_funcionamento']
        ]
        return Feirante(
            dados['email'],
            dados['senha'],
            localizacao,
            dados['nome_feira'],
            FormaContato[dados['forma_contato']],
            dados['contato'],
            dias_funcionamento,
        )