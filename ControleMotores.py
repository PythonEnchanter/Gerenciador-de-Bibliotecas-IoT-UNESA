import serial as pyard
import tkinter as tk
import random

file = open("log_interno.txt", mode="a")

lista_livros = []
lista_coords = []

for i in range (50):
    lista_livros.append(f"Título {i}")
    lista_coords.append([random.randint(0, 10), random.randint(0, 5)])

def sendData(data):
    data_parse = ";".join([f"{x}{y}" for x, y in data])
    try:
        ard_conn = pyard.Serial("COM5", 9600, timeout=1)
        ard_conn.write(data_parse.encode('utf-8'))
    except Exception as e:
        print(e)

def retrieveCoords(texto):
    return lista_coords[lista_livros.index(texto)]

root = tk.Tk()
lbl = tk.Label(root, text='Coordenadas do livro')
entry = tk.Entry(root)
btt = tk.Button(root, text='Enviar', command=lambda: sendData(retrieveCoords(entry.get())))
frame = tk.Frame(root, height=100, width=200, bg="beige")
lbl.pack()
btt.pack()
entry.pack()
frame.pack()

root.mainloop()