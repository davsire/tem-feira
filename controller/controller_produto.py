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
        unidade = dados['unidade'].replace('.', '').upper()  # Remova pontos, se necessário
        if unidade not in UnidadeProduto.__members__:
            raise ValueError(f"Unidade '{unidade}' não é válida.")
            
        produto = Produto(
            dados.get('_id'),
            dados['nome'],
            dados['preco'],
            dados.get('imagem'),
            dados['quantidade'],
            UnidadeProduto[dados['unidade']],
            self.__controller_main.controller_feirante.criar_feirante(dados['feirante']),
    )
    
        # Salve o produto no banco de dados
        self.__dao_produto.salvar_produto(produto)
        
        return produto
        
        

    def verificar_produtos_cesta_indisponiveis(self, produtos: list[ProdutoCesta]) -> bool:
        for produto in produtos:
            if self.__dao_produto.obter_produto_por_id(produto.produto.id).get('quantidade') < produto.quantidade:
                return True
        return False

    def decrementar_quantidade_produto(self, produto_id: str, quantidade: float):
        self.__dao_produto.decrementar_quantidade_produto(produto_id, quantidade)
