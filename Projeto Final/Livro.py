import Pacote

class Livro:
    def __init__(self, titulo, coord):
        self.titulo = titulo
        self.coord = coord

       #x---- Sys var ----x
        emprestado = False
        pacote = None
        endereco = None
        qtd_copias = 0
        cod_barras = None

       #x---- Obra var ----x
        autor = {'nome': None, 'editora': None}
        genero = {'genero': None, 'qtd_pagina': 0}

    '''def pacoteEmprestimo(self):
        pass'''