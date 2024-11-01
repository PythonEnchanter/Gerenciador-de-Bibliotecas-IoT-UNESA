import tkinter as tk
from xmlrpc.client import boolean

from PIL import Image, ImageTk
import sqlite3 as db
import Pacote, Admin, Livro, User, ContactInfo
import serial as pyard
from hashlib import sha1

#varíaveis relacionadas ao desenvolvimento do programa
version = "0.1a"
db_name = 'BiblioSys_db.db'

#variáveis referentes à customização da janela do programa
cursor_hover = "hand2"

#variáveis relacionadas à janela do programa
window_height = 600
window_width = 1000

class Sistema:
    def __init__(self):
        try:
            db_comm = db.connect(db_name)
            db_cursor = db_comm.cursor()

            db_cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                                 (cpf CHAR(10) PRIMARY KEY UNIQUE, nome VARCHAR(50), nascimento DATE, municipio VARCHAR(30), endereco VARCHAR(50), bairro VARCHAR(30), ddd INT, telefone INT, email VARCHAR(30))''')

            db_cursor.execute('''CREATE TABLE IF NOT EXISTS livros
                                 (isbn VARCHAR(10) PRIMARY KEY UNIQUE, titulo VARCHAR(50), autor VARCHAR(50), editora VARCHAR(20), genero VARCHAR(20), qtd_paginas INT)''')

            if db_comm: db_comm.close()
        except Exception as e:
            print("Erro ao conectar com o Banco de Dados")

    def iniciarAcessoDB(self, db_file):
        try:
            db_comm = db.connect(db_file);
        except Exception as e:
            print("Erro ao inicializar conexão com o Banco de Dados!\n")
        return db_comm

    def verifCredencial(self, senha):
        #verificação de credencial
        pass

    def verifChave(self, chave):
        #verificação de chave mestra
        pass

    def efetuaPacote(self, livros):
        #adiciona livros a um pacote por meio das hashs
        pacote = Pacote.Pacote()

class Popup:
    def __init__(self):
        self.root = tk.Toplevel()
        self.window_xcoord = (self.root.winfo_screenwidth() // 2) - (150 // 2)
        self.window_ycoord = (self.root.winfo_screenheight() // 2) - (110 // 2)
        self.root.geometry(f"150x110+{self.window_xcoord}+{self.window_ycoord}")
        self.root.title("Aviso - BiblioSys")

        self.label = tk.Label(self.root, text="Tem certeza que deseja finalizar o atendimento?", wraplength=100)

        self.continuar_btt = tk.Button(self.root, text="Continuar", bg="green", relief=tk.RAISED, foreground="white", command=self.continuar, cursor=cursor_hover, width=8)
        self.fechar_btt =  tk.Button(self.root, text="Sair", bg="red", relief=tk.RAISED, foreground="white", command=self.fechar, cursor=cursor_hover, width=8)

        self.label.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky=tk.W)
        self.continuar_btt.grid(row=1, column=0, columnspan=1)
        self.fechar_btt.grid(row=1, column=1, columnspan=1)


    def continuar(self):
        self.root.destroy()

    def fechar(self):
        self.root.destroy()
        root.destroy()

    def iniciar(self):
        self.root.mainloop()

class Window:
    def __init__(self, root):
        self.root = root
        window_xcoord = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        window_ycoord = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{window_xcoord}+{window_ycoord}")
        self.root.title(f"BiblioSys v{version}")
        self.root.configure(background="#bbb")
        self.tela_inicial = tk.Frame(self.root , width=window_width, height=window_height, bg='#bbb')
        self.tela_dados = tk.Frame(self.root , width=window_width, height=window_height, bg='#bbb')

        for frame in (self.tela_inicial, self.tela_dados):
            frame.grid(row=0, column=0, sticky="nsew")

        self.setTelaIncial()

    def setTelaIncial(self):
        #X--------------------- PRIMEIRA TELA -------------------------X
        #>_______________________ imagem ______________________________<
        try:
            self.img = Image.open("img/front_img_transp.png")
            self.front_img = ImageTk.PhotoImage(self.img.resize((600, 230)))
            self.front_img_label = tk.Label(self.tela_inicial, image=self.front_img, bg="#bbb", borderwidth=2, relief="raised")
        except FileNotFoundError:
            self.front_img_label = tk.Label(self.tela_inicial, text="BiblioSys - Sistema de Gerenciamento de Bilbiotecas Físicas")
        self.front_img_label.grid(column=0, row=0, columnspan=4, sticky="sew", pady=25, padx=200)
        #>_______________________ imagem ______________________________<

        #>_______________________ texto _______________________________<
        texto_inicio = tk.Label(self.tela_inicial)
        texto_inicio.configure(background="#aaa", text="Boas vindas à Biblioteca Social N1!\n\n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis purus nisl, efficitur vitae mauris sit amet, vehicula dapibus est. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse sit amet maximus sapien. Duis non est tellus. Maecenas sapien eros, porta vel ullamcorper non, egestas et lacus. Aliquam bibendum eleifend lacus, sit amet cursus dui sagittis eu. Sed tempor, neque in vehicula hendrerit, nisi sapien mollis lectus, ut molestie nulla quam nec mi. Integer suscipit mauris non dolor venenatis, sed placerat\n\n Desenvolvedor responsável: Bernardo Riper M. R. Dias", wraplength=600, justify="center")

        texto_inicio.grid(column=1, columnspan=2, padx=200)
        #>_______________________ texto _______________________________<

        #>_______________________ botões ______________________________<
        def onButtonClick(button):
            if button == "cadastrar":
                #tela de cadastro
                self.tela_dados.tkraise()
                self.setTelaDados()
            elif button == "atualizar":
                #verificação de credencial
                #tela de cadastro com user
                self.tela_dados.tkraise()
                self.setTelaDados()
            elif button == "consultar":
                #tela de acervo
                pass
            else:
                pop = Popup()
                pop.iniciar()

        btt_frame = tk.Frame(self.tela_inicial, bg="#bbb")

        cadastro_btt = tk.Button(btt_frame, text="Cadastrar Usuário", background="olive", foreground="white", command=lambda: onButtonClick("cadastrar"), width=15, relief="groove", cursor=cursor_hover)
        cadastro_btt.pack(side="left", padx=10)

        atualizar_btt = tk.Button(btt_frame, text="Atualizar Dados", background="brown", foreground="white", command=lambda: onButtonClick("atualizar"), width=15, relief="groove", cursor=cursor_hover)
        atualizar_btt.pack(side="left", padx=10)

        consulta_btt = tk.Button(btt_frame, text="Consultar Acervo", background="blue", foreground="white", command=lambda: onButtonClick("consultar"), width=15, relief="groove", cursor=cursor_hover)
        consulta_btt.pack(side="left", padx=10)

        fechar_btt = tk.Button(btt_frame, text="Finalizar", background="red", foreground="white", command=lambda: onButtonClick("finalizar"), width=15, relief="groove", cursor=cursor_hover)
        fechar_btt.pack(side="left", padx=10)

        btt_frame.grid(column=1, row=2, columnspan=2, pady=50)
        #>_______________________ botões ------------------------------<
        self.tela_inicial.tkraise()
        #X--------------------- PRIMEIRA TELA -------------------------x

    def setTelaDados(self):
        #X-------------------- TELA DE CREDENCIAL ---------------------x
        total_colunas = 0
        fields = ["cpf", "nome", "nascimento", "municipio", "endereco", "bairro", "ddd", "telefone", "email"]
        data = []
        fields = ", ".join(fields)

        campos = [
            #label, width, row, rowjmp/pass
            ("CPF: ", 15, 1, 0),
            ("Nome: ", 50, 1, 0),
            ("Nascimento: ", 10, 1, 0),
            ("Municipio: ", 20, 4, 1),
            ("Endereço: ", 30, 4, 1),
            ("Bairro: ", 20, 4, 1),
            ("DDD: ", 5, 7, 2),
            ("Telefone: ", 15, 7, 2),
            ("Email: ", 20, 7, 2),
            ("Senha: ", 20, 13, True),
            ("Confirmar senha: ", 20, 13, True)
        ]

        for i, field in enumerate(campos):
            label_text = field[0]
            largura = field[1]
            if type(field[3]) == int:
                max_columns = 3

                linha = field[2]+field[3]
                esconder = False
            else:
                linha = field[2]
                esconder = field[3]

            column = ((i % max_columns)) * 2

            label = tk.Label(self.tela_dados, text=label_text, bg="#bbb")
            label.grid(column=column, row=linha, padx=10, pady=20, sticky="w")

            entry = tk.Entry(self.tela_dados, width=largura, show="*" if esconder else "", bg="#fbb")
            data.append(entry)
            entry.grid(column=column+1 , row=linha, padx=10, pady = 20, sticky="w")

            total_colunas = column

        def enviaBD(field, data):
            data.pop()
            data.pop()
            data_to_insert = [entry.get() for entry in data]

            try:
                db_comm = Sistema.iniciarAcessoDB(self, db_name)
                db_cursor = db_comm.cursor()

                placeholder = ", ".join("?" for _ in data_to_insert)
                db_cursor.execute(f'''INSERT OR IGNORE INTO usuarios ({fields})
                                              VALUES ({placeholder})''', data_to_insert)

                db_comm.commit()
                db_comm.close()
            except db.OperationalError as e:
                print("Operational error:", e)
            except db.IntegrityError as e:
                print("Integrity error:", e)
            except db.ProgrammingError as e:
                print("Programming error:", e)
            except db.DatabaseError as e:
                print("Database error:", e)
            except db.InterfaceError as e:
                print("Interface error:", e)
            except db.Error as e:
                # Catch-all for any other sqlite3 errors
                print("An SQLite error occurred:", e)
            finally:
                if db_comm:
                    db_comm.close()
                    print("Database connection closed.")

            data.clear()
            raiseTelaInicial()

        def raiseTelaInicial():
            self.tela_inicial.tkraise()

        def raiseTelaDados(self):
            self.tela_dados.tkraise()

        cadastro_btt = tk.Button(self.tela_dados,
                                 text="Cadastrar Usuário",
                                 background="olive",
                                 foreground="white",
                                 command=lambda: enviaBD(fields, data),
                                 width=15,
                                 relief="groove",
                                 cursor=cursor_hover)
        cadastro_btt.grid(column=0, row=15, columnspan=2, padx=10)

        fechar_btt = tk.Button(self.tela_dados,
                               text="Tela Inicial",
                               background="red",
                               foreground="white",
                               command=lambda: raiseTelaInicial(),
                               width=15,
                               relief="groove",
                               cursor=cursor_hover)
        fechar_btt.grid(column=2, row=15, columnspan=2, padx=10)
        #X-------------------- TELA DE CREDENCIAL ---------------------x

if __name__ == "__main__":
    sis = Sistema()
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
