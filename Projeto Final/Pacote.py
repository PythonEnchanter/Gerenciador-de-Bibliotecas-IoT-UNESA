import hashlib

class Pacote:
    def __init__(self, cpf, lista_livros, data_pacote, data_pedido, data_devolve):
        self.cpf = cpf
        self.qtd_livros = len(lista_livros)
        self.lista_livros = lista_livros
        self.data_pacote = data_pacote
        self.data_pedido = data_pedido
        self.data_devolve = data_devolve
        self.cod_hash = None

    def efetuaPacote(self):
        #adiciona livros a um pacote por meio das hashs
        '''self.pacote.setPackHash
        self.user.pacote = self.pacote'''

    def setPackHash(self):
        self.cod_hash = hashlib.sha256(self.lista_livros.encode()).hexdigest()

    def getInfoPacote(self):
        info = []
        info.append(self.qtd_livros)
        info.append(self.lista_livros)
        info.append(self.data_pacote)
        info.append(self.data_pedido)

        return info