from dao.dao_produto import DaoProduto
from model.produto import Produto, UnidadeProduto
from model.produto_cesta import ProdutoCesta
from bson import ObjectId



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
        imagem_padrao = 'assets/img/produto_default.png'
        # print('Criando produto')
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

    def salvar_produto(self, dados: dict) -> str:
        # Validações
        if not dados['nome'] or not dados['nome'][0].isupper():
            return 'O nome do produto deve começar com letra maiúscula.'
        
        if not dados['nome'] or not dados['preco'] or not dados['quantidade'] or not dados['unidade']:
            return 'Todos os campos devem ser preenchidos.'
        
        try:
            dados['preco'] = float(dados['preco'])
            if dados['preco'] <= 0:
                return 'O preço deve ser maior que zero.'
        except ValueError:
            return 'Preço inválido! Por favor, insira um número válido.'
        
        try:
            dados['quantidade'] = float(dados['quantidade'])
            if dados['quantidade'] <= 0:
                return 'A quantidade deve ser maior que zero.'
        except ValueError:
            return 'Quantidade inválida! Por favor, insira um número válido.'
        
        feirante_id = dados['feirante']['_id']
        produto_existente = self.obter_produto_por_nome_e_feirante(dados['nome'].lower(), feirante_id)
        if produto_existente:
            return 'Este produto já existe no seu catálogo.'
        
        produto = self.criar_produto(dados)
        self.__dao_produto.inserir_produto(produto)
        return 'Produto salvo com sucesso!'
        
    def inserir_produto(self, produto: Produto):
        print(f'Inserindo produto {produto.nome.id} no banco de dados')
        documento = {
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "unidade": produto.unidade.name,
            "feirante": produto.feirante.id
        }
        self.__dao_produto.insert_one(documento)

    def editar_produto(self, dados: dict) -> str:
        # Validações
        if not dados['nome'] or not dados['nome'][0].isupper():
            return 'O nome do produto deve começar com letra maiúscula.'
        
        if not dados['nome'] or not dados['preco'] or not dados['quantidade'] or not dados['unidade']:
            return 'Todos os campos devem ser preenchidos.'
        
        try:
            dados['preco'] = float(dados['preco'])
            if dados['preco'] <= 0:
                return 'O preço deve ser maior que zero.'
        except ValueError:
            return 'Preço inválido! Por favor, insira um número válido.'
        
        try:
            dados['quantidade'] = float(dados['quantidade'])
            if dados['quantidade'] <= 0:
                return 'A quantidade deve ser maior que zero.'
        except ValueError:
            return 'Quantidade inválida! Por favor, insira um número válido.'
        
        produto = self.criar_produto(dados)
        query = {
            "nome": produto.nome,
            "feirante": ObjectId(produto.feirante.id)
        }
        update = {
            "$set": {
                "preco": produto.preco,
                "quantidade": produto.quantidade,
                "unidade": produto.unidade.name,
                "imagem": produto.imagem
            }
        }
        self.__dao_produto.update_one(query, update)
        return 'Produto editado com sucesso!'
        
    def obter_todos_produtos(self) -> list[Produto]:
        produtos = self.__dao_produto.find({})
        return produtos

    def obter_produto_por_nome_e_feirante(self, nome: str, feirante_id: str) -> Produto:
        produtos = self.obter_produtos_por_feirante(feirante_id, False)
        for produto in produtos:
            if produto.nome.lower() == nome.lower():
                return produto
        return None

    def excluir_produto(self, nome: str, feirante_id: str) -> str:
        if not nome:
            return 'Selecione um produto para excluir!'
        
        produto = self.obter_produto_por_nome_e_feirante(nome, feirante_id)
        if not produto:
            return 'Produto não encontrado!'
        
        self.__dao_produto.delete_one({'_id': ObjectId(produto.id)})
        return 'Produto excluído com sucesso!'