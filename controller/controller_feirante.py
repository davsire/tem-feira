import bcrypt
from dao.dao_feirante import DaoFeirante
from model.dia_funcionamento import DiaFuncionamento, DiaSemana
from model.feirante import Feirante, FormaContato
from model.localizacao import Localizacao
from service.service_geoapify import ServiceGeoapify


class ControllerFeirante:
    __instancia = None

    def __init__(self):
        self.__dao_feirante = DaoFeirante()
        self.__service_geoapify = ServiceGeoapify()

    def __new__(cls):
        if ControllerFeirante.__instancia is None:
            ControllerFeirante.__instancia = object.__new__(cls)
        return ControllerFeirante.__instancia

    def cadastrar_feirante(self, dados) -> Feirante:
        feirante = self.criar_feirante(dados)
        endereco = self.__service_geoapify.obter_endereco_por_lat_long(feirante.localizacao.latitude,
                                                                       feirante.localizacao.longitude)
        feirante.localizacao.endereco = endereco
        feirante.senha = bcrypt.hashpw(bytes(dados["senha"], 'utf-8'), bcrypt.gensalt())
        res = self.__dao_feirante.inserir_feirante(feirante)
        feirante.id = res.inserted_id
        return feirante

    def atualizar_feirante(self, id_feirante, dados) -> Feirante:
        feirante = self.criar_feirante(dados)
        endereco = self.__service_geoapify.obter_endereco_por_lat_long(feirante.localizacao.latitude,
                                                                       feirante.localizacao.longitude)
        feirante.localizacao.endereco = endereco
        feirante.senha = bcrypt.hashpw(bytes(dados["senha"], 'utf-8'), bcrypt.gensalt())
        feirante.id = id_feirante
        self.__dao_feirante.atualizar_feirante(feirante)
        return feirante

    def criar_feirante(self, dados) -> Feirante:
        localizacao = Localizacao(dados['localizacao']['latitude'], dados['localizacao']['longitude'])
        localizacao.endereco = dados['localizacao'].get('endereco', None)
        dias_funcionamento = [
            DiaFuncionamento(DiaSemana[dia['dia_semana']], dia['horario_abertura'], dia['horario_fechamento'])
            for dia in dados['dias_funcionamento']
        ]
        return Feirante(
            dados.get('_id'),
            dados['email'],
            dados['senha'],
            localizacao,
            dados['nome_feira'],
            FormaContato[dados['forma_contato']],
            dados['contato'],
            dias_funcionamento,
        )

    def logar_feirante(self, dados) -> Feirante | None:
        feirante_mongo = self.__dao_feirante.obter_feirante_por_email(dados["email"])
        if feirante_mongo is None:
            return None
        if bcrypt.checkpw(bytes(dados["senha"], 'utf-8'), feirante_mongo["senha"]):
            feirante = self.criar_feirante(feirante_mongo)
            return feirante

    def obter_feirante_por_email(self, email: str) -> Feirante | None:
        feirante_mongo = self.__dao_feirante.obter_feirante_por_email(email)
        if feirante_mongo is None:
            return None
        return self.criar_feirante(feirante_mongo)

    def excluir_feirante(self, feirante: Feirante):
        self.__dao_feirante.excluir_feirante(feirante)

    def obter_feirantes(self) -> list[Feirante]:
        feirantes_mongo = self.__dao_feirante.obter_feirantes()
        return [self.criar_feirante(feirante) for feirante in feirantes_mongo]

    def obter_feirante_por_nome(self, nome: str) -> Feirante | None:
        feirante_mongo = self.__dao_feirante.obter_feirante_por_nome(nome)
        if feirante_mongo is None:
            return None
        return self.criar_feirante(feirante_mongo)
