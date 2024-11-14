import tkinter as tk
from time import sleep, ctime
import serial as pyard
import hashlib, random, threading, ntplib

key = 1234567890
key_hash = hashlib.sha256(str(key).encode('utf-8')).hexdigest()

logfile = "BiblioSys_LOG.txt"

ard_port = "COM5"
ard_rate = 9600

class Connection:
    def __init__(self, porta, faixa):
        self.ard_conn = None

        try:
            self.ard_conn = pyard.Serial(port=porta, baudrate=faixa, timeout=1)
        except Exception as e:
            print(f"Erro de conexão... {e}")

        '''self.thread1 = threading.Thread(target=self.retrieveArdData)
        self.thread1.daemon = True
        self.thread1.start()'''

    #ISSO DEVE SER USADO NO ARDUINO
    '''def processar_dado(self, dado):
        tipo, valor = dado.split(':')
        tipo, message = tipo.split(';')
        
        #isso deve ser usado no arduino
        if tipo == 'T':
            print("Temperatura:", valor)
        elif tipo == 'H':
            print("Umidade:", valor)
        elif tipo == 'P':
            if message == 'M':
                pass
        elif tipo == 'S':
            self.sendUserData(valor)'''

    def requireStatusData(self):
        data_received = None

        try:
            self.ard_conn.write(f"K:{key_hash}".encode('utf-8'))
            return True
        except Exception as e:
            print(e)
            return False

    def sendUserData(self, data):
        if self.ard_conn is None:
            win.update_log(win.userlog_text, "Erro no sistema interno!!! Aguarde a chegada do Administrador.", False)
            return False
        else:
            try:
                win.update_log(win.userlog_text, "Pedido enviado ao sistema!", False)
                self.ard_conn.write(data)
                return True
            except Exception as e:
                print(e)
                return False

    def retrieveArdData(self):
        if self.ard_conn is None:
            print("Arduino não conectado!")
            return False
        else:
            data_buffer = []
            try:
                while self.ard_conn.in_waiting > 0:
                    print("WAITING")
                    ard_data = self.ard_conn.readline().decode('utf-8').strip()
                    data_buffer.append(ard_data)
                return data_buffer if data_buffer else None
            except Exception as e:
                print("err2")
                print(f"Dados não recebidos: {e}")
                return False

class Window:
    def __init__(self, root):
        self.lista_user = [] #livros selecionados pelo usuário para empréstimo
        self.lista_livros = [] #livros na biblioteca
        self.lista_btt = []
        self.lista_coords = [] #coordenadas de cada livro na estante

        self.root = root

        self.frame1 = tk.Frame(root, width=root.winfo_width())
        self.frame2 = tk.Frame(root, width=root.winfo_width())
        self.frame3 = tk.Frame(root, width=root.winfo_width())
        self.frame4 = tk.Frame(root, bg="white", width=root.winfo_width())
        self.frame5 = tk.Frame(root, bg="white", width=root.winfo_width())
        self.frame1.grid(column=0, row=0, columnspan=2, sticky="ew")
        self.frame2.grid(column=0, row=1, columnspan=2, sticky="ew")
        self.frame3.grid(column=0, row=2, columnspan=2, sticky="ew")
        self.frame4.grid(column=0, row=4, columnspan=5, sticky="ew")
        self.frame5.grid(column=0, row=6, columnspan=5, sticky="ew")

        cnt = 1
        for i in range(5):
            for j in range(5):
                btt_id = cnt
                btt = tk.Button(self.frame2, width=7, command=lambda btt_id=btt_id: self.OnButtonClick(f"Título {btt_id}"), text=f"Título {cnt}")
                coords = self.generateCoords()
                self.lista_livros.append(btt.cget('text'))
                while coords in self.lista_coords: #impede que dois livros tenham a mesma coordenada
                    coords = self.generateCoords()
                self.saveToLogFile(f"L: {btt.cget("text")} C: {coords}")
                self.lista_coords.append(coords)
                self.lista_btt.append(btt)
                btt.grid(row=i+1, column=j+1)
                cnt += 1

        id_lbl = tk.Label(self.frame1, text="ID: ")
        id_lbl.grid(column=0, row=0)
        self.id_entry = tk.Entry(self.frame1)
        self.id_entry.grid(column=1, row=0)

        self.booklog_lbl = tk.Label(self.root, text="Info. Livros")
        self.userlog_lbl = tk.Label(self.root, text="Info. Biblioteca")
        self.booklog_lbl.grid(column=0, row=3, sticky="w")
        self.userlog_lbl.grid(column=0, row=5, sticky="w")

        self.user_btts = []
        self.adm_btts = []
        entrar_btt = tk.Button(self.frame1, text="Entrar", command=lambda: self.OnButtonClick("Entrar"), width=15)
        pedido_btt = tk.Button(self.frame3, text="Realizar Pedido", command=lambda: self.OnButtonClick("Realizar Pedido"), width=15)
        parada_btt = tk.Button(self.frame3, text="Parar Operação", command=lambda: self.OnButtonClick("Parar Operação"), width=15)
        retomar_btt = tk.Button(self.frame3, text="Retomar Operação", command=lambda: self.OnButtonClick("Retomar Operação"), width=15)
        devolver_btt = tk.Button(self.frame3, text="Devolução de Livros", command=lambda: self.OnButtonClick("Devolução de Livros"), width=15)
        self.user_btts.extend([pedido_btt, devolver_btt])
        self.adm_btts.extend([parada_btt, retomar_btt])
        entrar_btt.grid(column=3, row=0)
        pedido_btt.grid(column=1, row=1, columnspan=2)
        parada_btt.grid(column=1, row=7, columnspan=2)
        retomar_btt.grid(column=3, row=7, columnspan=2)
        devolver_btt.grid(column=3, row=1, columnspan=2)

        self.booklog_text = tk.Text(self.frame4, wrap=tk.WORD, state="disabled", width=34, height=7, bg="white")
        self.userlog_text = tk.Text(self.frame5, wrap=tk.WORD, state="disabled", width=34, height=9, bg="white")

        self.booklog_scrollbar = tk.Scrollbar(self.frame4, orient=tk.VERTICAL)
        self.booklog_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.booklog_text.config(yscrollcommand=self.booklog_scrollbar.set)

        self.booklog_text.update_idletasks()
        self.booklog_text.rowconfigure(0, weight=1)
        self.booklog_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.booklog_text.pack(side=tk.LEFT)

        self.userlog_scrollbar = tk.Scrollbar(self.frame5, orient=tk.VERTICAL)
        self.userlog_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.userlog_text.config(yscrollcommand=self.userlog_scrollbar.set)

        self.userlog_text.update_idletasks()
        self.userlog_text.rowconfigure(0, weight=1)
        self.userlog_text.pack(side=tk.LEFT)

        self.booklog_text.yview_pickplace("end")
        self.userlog_text.yview_pickplace("end")

        self.update_log(self.userlog_text, "Arduino", True)
        self.update_log(self.booklog_text, "Livros Selecionados", True)

        self.disableButtons(self.user_btts)
        self.disableButtons(self.adm_btts)

    def getTime(self):
        client = ntplib.NTPClient()

        try:
            response = client.request('pool.ntp.org')
            utc_time = ctime(response.tx_time)
            return utc_time
        except Exception as e:
            print(e)
            return "NTP Server not connected"

    def disableButtons(self, buttons):
        for i in iter(buttons):
            i.configure(state="disabled")

    def enableButtons(self, buttons):
        for i in iter(buttons):
            i.configure(state="active")

    def OnButtonClick(self, text):
        if text == "Entrar":
            if self.id_entry.get() == "user":
                self.enableButtons(self.user_btts)
                self.id_entry.delete(0, tk.END)
                self.update_log(self.userlog_text, "\nUser logado com sucesso!", False)
            elif self.hashEntry(self.id_entry.get()) == key_hash:
                self.enableButtons(self.adm_btts)
                self.id_entry.delete(0, tk.END)
                self.update_log(self.userlog_text, "\nAdmin logado com sucesso!", False)
            else:
                self.update_log(self.userlog_text, "\nUsuário não encontrado", False)
        elif text == "Realizar Pedido":
            print(self.lista_user)
            if not self.lista_user:
                self.update_log(self.userlog_text, "\nNenhum livro selecionado!", False)
            else:
                livros_user_coords = []
                envio_coord = None

                self.lista_user = list(set(self.lista_user)) #retira duplicatas
                for i in self.lista_user: #separa as coordenadas dos livros selecionados
                    livros_user_coords.append(self.lista_coords[self.lista_livros.index(i)])
                print(f">>>  E:{livros_user_coords}".encode('utf-8'))
                envio_coord = ";".join([f"{x}{y}" for x, y in livros_user_coords])
                if ard_conn.sendUserData(f"E:{envio_coord}".encode('utf-8')):

                    ard_return = ard_conn.retrieveArdData()
                    if ard_return == False:
                        pass

                    self.update_log(self.userlog_text, ard_return.decode('utf-8'), False)
                    self.update_log(self.booklog_text, f"{self.lista_user}\nTotal de livros: {len(self.lista_user)}\nAguarde a entrega do seu pedido!", True)
                    self.update_log(self.userlog_text, )
                else:
                    self.update_log(self.booklog_text, f"Livros selecionados:\n{self.lista_user}", True)
                    self.update_log(self.booklog_text, "Seu pedido será efetuado futuramente...", False)
                sleep(0.1)
                print(f" Arduino: {ard_conn.retrieveArdData()}")
        elif text == "Parar Operação":
            ard_conn.sendUserData(["P"])
        elif text == "Retomar Operação":
            ard_conn.sendUserData(["R"])
        elif text == "Devolução de Livros":
            self.update_log(self.userlog_text, "\nPor favor, coloque os livros na esteira.", False)
            ard_conn.sendUserData(["D"])
        else:
            self.lista_user.append(text)
            self.update_log(self.booklog_text, f"Livros selecionados:\n{self.lista_user}", True)

    def saveToLogFile(self, message):
        file = open(logfile, mode='a')
        file.write(message + "\n")

    def update_log(self, log_widget, message, state):
        log_widget.config(state="normal")
        if state:
            log_widget.delete("1.0", tk.END)
        log_widget.insert(tk.END, f"\n{message}")
        log_widget.config(state="disabled")

        self.saveToLogFile(f"{self.getTime()} || Objeto: " + str(log_widget) + ": " + message + "\n")

    def hashEntry(self, entry):
        return hashlib.sha256(str(entry).encode('utf-8')).hexdigest()

    def generateCoords(self):
        xcoord = random.randint(0, 4)
        ycoord = random.randint(0, 4)

        return [xcoord, ycoord]

ard_conn = Connection(ard_port, ard_rate)

root = tk.Tk()
root.geometry('295x550')
root.title('Arduino de Bibliotecas')
root.resizable(False, False)
win = Window(root)
root.mainloop()