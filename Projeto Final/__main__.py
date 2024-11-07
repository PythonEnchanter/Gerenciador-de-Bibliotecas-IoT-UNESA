import tkinter as tk
from PIL import Image, ImageTk
import sqlite3 as db
import Pacote, Admin, Livro, ContactInfo
from User import User
import serial as pyard
import hashlib

#varíaveis relacionadas ao desenvolvimento do programa
version = "0.1a"
db_name = 'BiblioSys_db.db'

#variáveis referentes à customização da janela do programa
cursor_hover = "hand2"

#variáveis relacionadas à janela do programa
window_height = 610
window_width = 1000

class Sistema:
    def __init__(self):
        self.user = None
        try:
            db_comm = db.connect(db_name)
            db_cursor = db_comm.cursor()

            db_cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                                 (cpf CHAR(10) PRIMARY KEY UNIQUE, nome VARCHAR(50), nascimento DATE, municipio VARCHAR(30), endereco VARCHAR(50), bairro VARCHAR(30), ddd INT, telefone INT, email VARCHAR(30), password VARCHAR(60))''')

            db_cursor.execute('''CREATE TABLE IF NOT EXISTS livros
                                 (isbn VARCHAR(10) PRIMARY KEY UNIQUE, titulo VARCHAR(50), autor VARCHAR(50), editora VARCHAR(20), genero VARCHAR(20), qtd_paginas INT)''')

            if db_comm: db_comm.close()
        except Exception as e:
            print("Erro ao conectar com o Banco de Dados")

    def instUser(self, cpf):
        #os campos endereco e bairro devem vir em uma string, separados por vírgula
        #os campos ddd e telefone devem vir em uma string, juntos
        db_data = self.recebeDB(cpf)
        db_treat = []

        for i in db_data:
            db_treat.append(i)

        print(f"Pre 1: {db_treat}")
        db_treat.pop()

        print(f"Pos 1: {db_treat}")
        db_treat[3] = db_treat[4] + ', ' +  db_treat[5] + ', ' + db_treat[3]
        db_treat.pop(4)
        db_treat.pop(4)

        print(f"Pos 2: {db_treat}")
        db_treat[4] = str(db_treat[4]) + str(db_treat[5])
        db_treat.pop(5)

        print(f"{db_treat} {db_treat[-2]}")
        self.user = User(*db_treat)

    def getUserCPF(self):
        return self.user.cpf

    def iniciarAcessoDB(self, db_file):
        try:
            db_comm = db.connect(db_file)
        except Exception as e:
            print("Erro ao inicializar conexão com o Banco de Dados!\n")
        return db_comm

    def enviaBD(self, field, data, sis):
        for i in range(len(data)):
            data[i] = data[i].get()

        if data[-1] != data[-2]:
            pop = Popup("senha")
            pop.dataError()
        else:
            pass

        data.pop()
        print(data[-2])
        data[-1] = hashlib.sha256(data[-1].encode('utf-8')).hexdigest()
        data_to_insert = [entry for entry in data]

        db_comm = None
        try:
            db_comm = Sistema.iniciarAcessoDB(db_name, db_name)
            db_cursor = db_comm.cursor()

            db_cursor.execute("PRAGMA table_info(usuarios)")
            print(db_cursor.fetchall())

            for i in data: print(i)
            placeholder = ", ".join("?" for _ in data_to_insert)
            db_cursor.execute(f'''INSERT OR REPLACE INTO usuarios ({field})
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
            print("An SQLite error occurred:", e)
        finally:
            if db_comm:
                db_comm.close()
                print("Database connection closed.")

        data.clear()
        window = Window(root, sis)
        window.raiseTelaInicial()

    def recebeDB(self, cpf):
        db_comm = self.iniciarAcessoDB(db_name)
        db_cursor = db_comm.cursor()

        try:
            db_cursor.execute(f'''SELECT * FROM usuarios WHERE cpf = ?''', (cpf,))
            return db_cursor.fetchone()
        except Exception as e:
            print(e)
            return None
        finally:
            db_comm.close()

    def deletarRegistroDB(self, cpf):
        db_comm = self.iniciarAcessoDB(db_name)
        db_cursor = db_comm.cursor()

        try:
            db_cursor.execute(f'''DELETE FROM usuarios WHERE cpf = ?''', (cpf,))
            db_comm.commit()
        except Exception as e:
            print("Erro")
            print(e)

    def verifCredencial(self, cpf, senha):
        #verificação de credencial
        db_comm = self.iniciarAcessoDB(db_name)
        db_cursor = db_comm.cursor()

        data = self.recebeDB(cpf)

        if data == None: #usuário não encontrado
            pop = Popup("user")
        elif hashlib.sha256(senha.encode('utf-8')).hexdigest() != data[-1]: #senha errada
            pop = Popup("senha")
        else:
            return True

    def verifChave(self, chave):
        #verificação de chave mestra
        pass

    def efetuaPacote(self, livros):
        #adiciona livros a um pacote por meio das hashs
        pacote = Pacote.Pacote()

class Popup:
    def __init__(self, estilo):
        self.root = tk.Toplevel()
        self.window_xcoord = (self.root.winfo_screenwidth() // 2) - (150 // 2)
        self.window_ycoord = (self.root.winfo_screenheight() // 2) - (110 // 2)
        self.root.geometry(f"150x110+{self.window_xcoord}+{self.window_ycoord}")
        self.root.title("Aviso - BiblioSys")

        if estilo == "fechar":
            self.terminatePop()
        elif estilo == "senha":
            self.dataError(estilo)
        elif estilo == "user":
            self.dataError(estilo)

    def dataError(self, reason):
        if reason == "senha":
            self.label = tk.Label(self.root, text="As senhas não são iguais", wraplength=100)
        elif reason == "user":
            self.label = tk.Label(self.root, text="Usuário não cadastrado no Banco de Dados", wraplength=100)

        self.continuar_btt = tk.Button(self.root,
                                       text="Retornar",
                                       bg="green",
                                       relief=tk.RAISED,
                                       foreground="white",
                                       command=self.continuar,
                                       cursor=cursor_hover,
                                       width=8)

        self.label.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky=tk.W)
        self.continuar_btt.grid(row=1, column=0, columnspan=1)

    def terminatePop(self):
        self.label = tk.Label(self.root, text="Tem certeza que deseja finalizar o atendimento?", wraplength=100)

        self.continuar_btt = tk.Button(self.root,
                                       text="Continuar",
                                       bg="green",
                                       relief=tk.RAISED,
                                       foreground="white",
                                       command=self.continuar,
                                       cursor=cursor_hover,
                                       width=8)
        self.fechar_btt = tk.Button(self.root,
                                    text="Sair",
                                    bg="red",
                                    relief=tk.RAISED,
                                    foreground="white",
                                    command=self.fechar,
                                    cursor=cursor_hover,
                                    width=8)

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
    def __init__(self, root, sis):
        self.root = root
        window_xcoord = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        window_ycoord = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{window_xcoord}+{window_ycoord}")
        self.root.title(f"BiblioSys v{version}")
        self.root.configure(background="#bbb")
        self.tela_inicial = tk.Frame(self.root , width=window_width, height=window_height, bg='#bbb')
        self.tela_dados = tk.Frame(self.root , width=window_width, height=window_height, bg='#bbb')
        self.tela_login = tk.Frame(self.root, width=window_width, height=window_height, bg='#bbb')
        self.tela_acervo = tk.Frame(self.root, width=window_width, height=window_height, bg='#bbb')
        self.sis = sis

        for frame in (self.tela_inicial, self.tela_dados, self.tela_login, self.tela_acervo):
            frame.grid(row=0, column=0, sticky="nsew")

        self.setTelaInicial()

    def setTelaInicial(self):
        #>_______________________ imagem ______________________________<
        try:
            self.img = Image.open("img/front_img_transp.png")
            self.front_img = ImageTk.PhotoImage(self.img.resize((600, 230)))
            self.front_img_label = tk.Label(self.tela_inicial, image=self.front_img, bg="#bbb", borderwidth=2, relief="raised")
        except FileNotFoundError:
            self.front_img_label = tk.Label(self.tela_inicial, text="BiblioSys - Sistema de Gerenciamento de Bibliotecas Físicas")
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
                self.raiseTelaDados(button)
            elif button == "atualizar":
                #verificação de credencial
                #tela de cadastro com user
                self.raiseTelaLogin(button)
            elif button == "consultar":
                #tela de acervo
                self.raiseTelaLogin(button)
            else:
                pop = Popup("fechar")
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

    def setTelaDados(self, action):
        #X-------------------- TELA DE CREDENCIAL ---------------------x
        total_colunas = 0
        fields = ["cpf", "nome", "nascimento", "municipio", "endereco", "bairro", "ddd", "telefone", "email", "password"]
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
            ("Email: ", 30, 7, 2),
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

        if action == "cadastrar":
            cadastro_btt = tk.Button(self.tela_dados,
                                     text="Cadastrar Usuário",
                                     background="olive",
                                     foreground="white",
                                     command=lambda: sis.enviaBD(fields, data, sis),
                                     width=15,
                                     relief="groove",
                                     cursor=cursor_hover)
            cadastro_btt.grid(column=0, row=15, columnspan=2, padx=10)
        else:

            #insere os dados do usuarios nas Entries
            u_data = self.sis.recebeDB(sis.getUserCPF())
            for j, i in enumerate(data):
                print(f"TAMANHOS {len(u_data)} {len(data)}\n")
                if j > len(u_data)-2: #exige que o usuário coloque a senha novamente antes de deletar
                    pass
                else:
                    print(f"III: {i} JJJ: {j} UUU: {u_data[j]}")
                    i.delete(0, tk.END)
                    i.insert(0, f"{u_data[j]}")

            update_btt = tk.Button(self.tela_dados,
                                   text="Atualizar cadastro",
                                   background="olive",
                                   foreground="white",
                                   command=lambda: sis.enviaBD(fields, data, sis),
                                   width=15,
                                   relief="groove",
                                   cursor=cursor_hover)
            update_btt.grid(column=0, row=15, columnspan=2, padx=10)

            delete_btt = tk.Button(self.tela_dados,
                                   text="Deletar cadastro",
                                   background="olive",
                                   foreground="white",
                                   command=lambda: sis.deletarRegistroDB(sis.getUserCPF()),
                                   width=15,
                                   relief="groove",
                                   cursor=cursor_hover)
            delete_btt.grid(column=2, row=15, columnspan=2, padx=10)

        fechar_btt = tk.Button(self.tela_dados,
                               text="Tela Inicial",
                               background="red",
                               foreground="white",
                               command=lambda: self.raiseTelaInicial(),
                               width=15,
                               relief="groove",
                               cursor=cursor_hover)
        fechar_btt.grid(column=4, row=15, columnspan=2, padx=10)
        #X-------------------- TELA DE CREDENCIAL ---------------------x

    def setTelaLogin(self, comando):
        def onButtonClick(button):
            if button.cget("text") == "Entrar":
                print(f"cpf: {cpf_ety.get()} senha {senha_ety.get()}")
                if self.sis.verifCredencial(cpf_ety.get(), senha_ety.get()):
                    if comando == "atualizar":
                        self.sis.instUser(cpf_ety.get())
                        self.raiseTelaDados(comando)
                    elif comando == "consultar":
                        self.sis.instUser(cpf_ety.get())
                        self.raiseTelaAcervo()
            else:
                pass

        cpf_lbl = tk.Label(self.tela_login, text="CPF: ")
        senha_lbl = tk.Label(self.tela_login, text="Senha: ")

        cpf_ety = tk.Entry(self.tela_login, width=20, bg="#fbb")
        senha_ety = tk.Entry(self.tela_login, width=20, show="*", bg="#fbb")

        cpf_lbl.grid(column=0, row=0, columnspan=2, padx=10)
        cpf_ety.grid(column=2, row=0, columnspan=2, padx=10)
        senha_lbl.grid(column=4, row=0, columnspan=2, padx=10)
        senha_ety.grid(column=6, row=0, columnspan=2, padx=10)

        entrar_btt = tk.Button(self.tela_login,
                               text="Entrar",
                               background="green",
                               foreground="black",
                               command=lambda: onButtonClick(entrar_btt),
                               width=15,
                               relief="groove",
                               cursor=cursor_hover)
        entrar_btt.grid(column=2, row=2, columnspan=2, padx=10, pady=10)

        voltar_btt = tk.Button(self.tela_login,
                               text="Voltar",
                               background="red",
                               foreground="white",
                               command=lambda: self.raiseTelaInicial(),
                               width=15,
                               relief="groove",
                               cursor=cursor_hover)
        voltar_btt.grid(column=4, row=2, columnspan=2, padx=10, pady=10)

    def setTelaAcervo(self):
        def onButtonPress(button):
            if button.cget("text") == "":
                pass
        #separador visual
        coluna1_frame = tk.Frame(self.tela_acervo, width=window_width * 0.7, height=600, bg='#bbb')
        coluna2_frame = tk.Frame(self.tela_acervo, width=window_width * 0.3, height=600, bg='#bbb')
        coluna1_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")
        coluna2_frame.grid(column=2, row=0, columnspan=2, sticky="nsew")

        #separadores dos blocos
        acervo_frame = tk.Frame(coluna1_frame, bg="#666", width=(window_width * 0.7) - 20, height=440)
        userinf_frame = tk.Frame(coluna2_frame, bg="#666", width=(window_width * 0.3) - 20, height=290)
        bookinf_frame = tk.Frame(coluna1_frame, bg="#666", width=(window_width * 0.7) - 20, height=140)
        button_frame = tk.Frame(coluna2_frame, bg="#666", width=(window_width * 0.3) - 20, height=290)
        acervo_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        bookinf_frame.grid(column=0, row=1, columnspan=2, padx=10, sticky="nsew")
        userinf_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        button_frame.grid(column=0, row=1, columnspan=2, padx=10, sticky="nsew")
        coluna1_frame.grid_rowconfigure(0, weight=1)
        coluna1_frame.grid_columnconfigure(0, weight=1)
        coluna2_frame.grid_rowconfigure(0, weight=1)
        coluna2_frame.grid_columnconfigure(0, weight=1)

        #canvas interno de acervo_frame
        cv_book_selection = tk.Canvas(acervo_frame, bg="white")
        cv_book_selection.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar = tk.Scrollbar(acervo_frame, orient=tk.VERTICAL, command=cv_book_selection.yview, width=20)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        cv_book_selection.configure(yscrollcommand=v_scrollbar.set)
        bookslct_frame = tk.Frame(cv_book_selection)
        cv_book_selection.create_window((0, 0), window=bookslct_frame, anchor="nw")
        acervo_button_list = []
        for i in range(5):
            for j in range(10):
                btt = tk.Button(bookslct_frame, text=f"Titulo {(i + 1) * (j + 1)}", width=15, height=10)
                btt.grid(column=i, row=j, padx=9, pady=5, sticky="nsew")
                acervo_button_list.append(btt)
        bookslct_frame.update_idletasks()
        cv_book_selection.config(scrollregion=cv_book_selection.bbox("all"))

        acervo_title_lbl = tk.Label(acervo_frame, text="Listagem")
        userinf_title_lbl = tk.Label(userinf_frame, text="Dados de Usuário")
        bookinf_title_lbl = tk.Label(bookinf_frame, text="Dados do Livro")

        #-----------------------------user-------------------------------#


        #------------------------------btt-------------------------------#
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)

        emprestimo_btt = tk.Button(button_frame, text="Realizar pedido")
        devolver_btt = tk.Button(button_frame, text="Devolução de livros")
        consulta_btt = tk.Button(button_frame, text="Consultar pedido")
        voltar_btt = tk.Button(button_frame, text="Tela Inicial")
        emprestimo_btt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        devolver_btt.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        consulta_btt.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        voltar_btt.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)

    def raiseTelaInicial(self):
        self.tela_inicial.tkraise()

    def raiseTelaDados(self, comando):
        self.setTelaDados(comando)
        self.tela_dados.tkraise()

    def raiseTelaAcervo(self):
        self.setTelaAcervo()
        self.tela_acervo.tkraise()

    def raiseTelaLogin(self, comando):
        self.setTelaLogin(comando)
        self.tela_login.tkraise()

    def AtualizarDados(self, cpf):
        #função para abrir a tela de cadastro com os dados do usuário
        '''Etapas:
           0: Verificar credencial
           1: Puxar dados do DB
           2: Exibir dados nos fields
           3: Proteger CPF e senha
           3: Gerar botões de modificar e cancelar
           4: Alterar dados no DB
        '''
        pass

if __name__ == "__main__":
    sis = Sistema()
    root = tk.Tk()
    app = Window(root, sis)
    root.mainloop()