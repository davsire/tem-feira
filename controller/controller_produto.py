from dao.dao_produto import DaoProduto
from model.produto import Produto, UnidadeProduto
from model.produto_cesta import ProdutoCesta


class ControllerProduto:
    __instancia = None

    def __init__(self, controller_main):
        self.__dao_produto = DaoProduto()
        self.__controller_main = controller_main

    def __new__(cls, *args):
        if ControllerProduto.__instancia is None:
            ControllerProduto.__instancia = object.__new__(cls)
        return ControllerProduto.__instancia

    def obter_produtos_por_feirante(self, feirante_id: str, apenas_disponiveis: bool) -> list[Produto]:
        produtos_mongo = self.__dao_produto.obter_produtos_por_feirante(feirante_id, apenas_disponiveis)
        return [self.criar_produto(produto) for produto in produtos_mongo]

    def excluir_produtos_por_feirante(self, feirante_id: str):
        self.__dao_produto.excluir_produtos_por_feirante(feirante_id)

    def criar_produto(self, dados: dict) -> Produto:
        imagem_padrao = '/home/ale-vasco/ale/UFSC/APS/tem-feira/assets/img/icone-produto.png'
        print('Criando produto')
        return Produto(
            dados.get('_id'),
            dados['nome'],
            dados['preco'],
            dados.get('imagem', imagem_padrao),
            dados['quantidade'],
            UnidadeProduto[dados['unidade']],
            self.__controller_main.controller_feirante.criar_feirante(dados['feirante']),
        )

    def verificar_produtos_cesta_indisponiveis(self, produtos: list[ProdutoCesta]) -> bool:
        for produto in produtos:
            if self.__dao_produto.obter_produto_por_id(produto.produto.id).get('quantidade') < produto.quantidade:
                return True
        return False

    def decrementar_quantidade_produto(self, produto_id: str, quantidade: float):
        self.__dao_produto.decrementar_quantidade_produto(produto_id, quantidade)

    def salvar_produto(self, dados: dict):
        produto = self.criar_produto(dados)
        self.__dao_produto.inserir_produto(produto)
        print('Produto salvo no banco de dados!')
        
    def obter_todos_produtos(self):
        return list(self.__dao_produto.find({}))

    def obter_produto_por_nome(self, nome: str):
        return self.__dao_produto.find_one({'nome': nome.lower()})    