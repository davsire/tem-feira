from bson import ObjectId
from dao.dao_cesta import DaoCesta
from model.cesta import Cesta
from model.produto_cesta import ProdutoCesta


class ControllerCesta:
    __instancia = None

    def __init__(self, controller_main):
        self.__dao_cesta = DaoCesta()
        self.__controller_main = controller_main

    def __new__(cls, *args):
        if ControllerCesta.__instancia is None:
            ControllerCesta.__instancia = object.__new__(cls)
        return ControllerCesta.__instancia

    def obter_cestas_por_feirante(self, feirante_id: str) -> list[Cesta]:
        cestas_mongo = self.__dao_cesta.obter_cestas_por_feirante(feirante_id)
        return [self.criar_cesta(cesta) for cesta in cestas_mongo]

    def excluir_cestas_por_feirante(self, feirante_id: str):
        cestas = self.__dao_cesta.find({'feirante': ObjectId(feirante_id)})
        for cesta in cestas:
            self.__controller_main.controller_reserva.excluir_reserva_por_cesta(cesta.get('_id'))
        self.__dao_cesta.excluir_cestas_por_feirante(feirante_id)

    def criar_cesta(self, dados: dict) -> Cesta:
        return Cesta(
            dados.get('_id'),
            dados['nome'],
            [
                ProdutoCesta(
                    self.__controller_main.controller_produto.criar_produto(produto['produto']),
                    produto['quantidade']
                )
                for produto in dados['produtos']
            ],
            dados['preco_total'],
            dados['personalizada'],
            dados['reservada'],
            self.__controller_main.controller_feirante.criar_feirante(dados['feirante']),
        )

    def criar_cesta_pronta(self, dados: dict) -> Cesta:
        return Cesta(
            dados.get('_id'),
            dados['nome'],
            [
                ProdutoCesta(
                    chave,
                    valor
                )
                for chave, valor in dados['produtos_id'].items()
            ],
            dados['preco_total'],
            dados['personalizada'],
            dados['reservada'],
            dados['feirante_id']
        )

    def cadastrar_cesta_pronta(self, dados: dict):
        cesta = self.criar_cesta_pronta(dados)
        self.__dao_cesta.inserir_cesta(cesta)

    def verificar_cesta_reservada(self, cesta_id: str) -> bool:
        return self.__dao_cesta.obter_cesta_por_id(cesta_id).get('reservada')

    def marcar_cesta_reservada(self, cesta_id: str, reservada: bool):
        self.__dao_cesta.marcar_cesta_reservada(cesta_id, reservada)

    def excluir_cesta(self, cesta: Cesta):
        self.__dao_cesta.excluir_cesta(cesta)