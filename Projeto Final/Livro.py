import Pacote

class Livro:
    def __init__(self, titulo, coord):
        self.titulo = titulo
        self.coord = coord

       #x---- Sys var ----x
        self.emprestado = False
        self.pacote = None
        self.endereco = None
        self.qtd_copias = 0
        self.cod_barras = None

       #x---- Obra var ----x
        autor = {'nome': None, 'editora': None}
        genero = {'genero': None, 'qtd_pagina': 0}

    def getEmprestimoInfo(self):
        return self.emprestado

    def pacoteEmprestimo(self):
        pass