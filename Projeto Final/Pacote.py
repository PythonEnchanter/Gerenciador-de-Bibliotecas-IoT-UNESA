class Pacote:
    def __init__(self, cpf, qtd_livros, lista_livros, data_pacote, data_pedido, data_devolve):
        self.cpf = cpf
        self.qtd_livros = qtd_livros
        self.lista_livros = lista_livros
        self.data_pacote = data_pacote
        self.data_pedido = data_pedido
        self.data_devolve = data_devolve

        codigo_hash = None