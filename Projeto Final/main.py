import tkinter as tk
from PIL import Image, ImageTk

#varíaveis relacionadas ao desenvolvimento do programa
version = "0.1a"

#variáveis referentes à customização da janela do programa
cursor_hover = "hand2"

#variáveis relacionadas à janela do programa
root = tk.Tk()
window_height = 600
window_width = 1000
window_xcoord = (root.winfo_screenwidth() // 2) - (window_width // 2)
window_ycoord = (root.winfo_screenheight() // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{window_xcoord}+{window_ycoord}")
root.title(f"BiblioSys v{version}")
root.configure(background="#bbb")
'''root.bind("<KeyPress>", keyPress)'''

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

#X-------------------------- PRIMEIRA TELA --------------------------x
#>_______________________ imagem ______________________________<
try:
    img = Image.open("img/front_img_transp.png")
    front_img = ImageTk.PhotoImage(img.resize((600, 230)))

    front_img_label = tk.Label(root, image=front_img, bg="#bbb", borderwidth=2, relief="raised")
except FileNotFoundError:
    front_img_label = tk.Label(root, text="BiblioSys - Sistema de Gerenciamento de Bilbiotecas Físicas")
front_img_label.grid(column=0, row=0, columnspan=4, sticky="sew", pady=25, padx=200)
#>_______________________ imagem ______________________________<

#>_______________________ texto ______________________________<
texto_inicio = tk.Label(root)
texto_inicio.configure(background="#aaa", text="Boas vindas à Biblioteca Social N1!\n\n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis purus nisl, efficitur vitae mauris sit amet, vehicula dapibus est. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse sit amet maximus sapien. Duis non est tellus. Maecenas sapien eros, porta vel ullamcorper non, egestas et lacus. Aliquam bibendum eleifend lacus, sit amet cursus dui sagittis eu. Sed tempor, neque in vehicula hendrerit, nisi sapien mollis lectus, ut molestie nulla quam nec mi. Integer suscipit mauris non dolor venenatis, sed placerat\n\n Desenvolvedor responsável: Bernardo Riper M. R. Dias", wraplength=600, justify="center")

texto_inicio.grid(column=1, columnspan=2, padx=200)
#>_______________________ texto ______________________________<

#>_______________________ botões ______________________________<
def onButtonClick(button):
    if button == "cadastrar":
        #tela de cadastro
        pass
    elif button == "atualizar":
        #verificação de credencial
        #tela de cadastro com user
        pass
    elif button == "consultar":
        #tela de acervo
        pass
    else:
        pop = Popup()
        pop.iniciar()

btt_frame = tk.Frame(root, bg="#bbb")

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
#X-------------------------- PRIMEIRA TELA --------------------------x

#X-------------------------- TELA DE CREDENCIAL ---------------------x



#X-------------------------- TELA DE CREDENCIAL ---------------------x
root.mainloop()
