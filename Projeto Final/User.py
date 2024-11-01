import ContactInfo as cnt_info

class User:
    def __init__(self, cpf, nome, domicilio, telefone, email, nascimento, senha, pacote_ativo):
        self.cpf = cpf
        self.nome = nome
        self.domicilio = domicilio
        self.telefone = cnt_info.cellphoneNumber(telefone)
        self.email = cnt_info.enderecoEmail(email)
        self.nascimento = nascimento

        lista_leitura = []
        lista_desejo = []
        lista_pacote = []
        restrito = False
        qtd_livros = 3

    def cadastrar(self):
        #envia para o banco de dados
        pass

    def consultarEmprestimo(self):
        #retorna o conjunto de livros so pacote de empréstimo ativo
        pass

    def pedirEmprestimo(self):
        #executa o pacote de empréstimo pendente
        pass

    def devolverLivros(self):
        #retorna os livros emprestados
        pass

    def atualizarCadastro(self):
        #altera as informações no banco de dados
        pass

    def consultarAcervo(self):
        #leva o usuario até a página de consulta de livros
        pass

    def addQtdRestrito(self):
        #adiciona restrição de quantidades de livros por empréstimo
        pass

    def addPctRestrito(self):
        #adciona restrição de quantidade de pacotes ativos
        pass