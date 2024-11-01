import ContactInfo as cnt_info

class Admin:
    def __init__(self, nome, cpf, telefone, email, senha, chave_mestra, acesso_db):
        self.nome = nome
        self.cpf = cpf
        self.telefone = cnt_info.cellphoneNumber(telefone)
        self.email = cnt_info.emailAddress(email)
        self.senha = senha
        self.chave_mestra = chave_mestra
        self.acesso_db = acesso_db

    def cadastrarLivro(self):
        #acesso_db
        #permite o cadastro de livros no acervo interno
        # essa função precisa que o sistema interno receba os livros informados (funciona como uma devolução)
        pass

    def consultarAcervo(self):
        #chave_mestra
        #fornece dados críticos sobre o acervo
        pass

    def removerlivros(self ):
        #acesso_db
        #chave_mestra
        #retira livros do acervo
        #essa função precisa que o sistema interno retire os livros informados e entregue ao administrador (funciona como um empréstimo ilimitado)
        pass

    def contatoUsuario(self, usuario, metodo):
        #entra em contato com o usuário informado
        pass

    def pararFuncionamento(self):
        #chave_mestra
        #interrompe o funcionamento do sistema para manutenção
        pass