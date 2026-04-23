import tkinter as tk
from tkinter import Button

def enquadramento(m, n):
    label = tk.Label(tela1, text="=" * 13, font=("Terminal", 30), bg="blue", fg="white")
    label.grid(column=m, row=n, pady=5)

def mostrar_tela(tela):
    for frame in [tela1, tela_jogo, tela_podio, tela_pergun1N]:
        frame.pack_forget()
    tela.pack(fill="both", expand=True)

def salvar_nomeN():
    nome=entrada_nome.get()
    with open("PodioN.txt", "a") as arquivo:
        arquivo.write(nome+"\n")

def salvar_nomeR():
    nome = entrada_nome.get()
    with open("PodioR.txt", "a") as arquivo:
        arquivo.write(nome + "\n")

def salvar_nome_podio_N():
    with open("PodioN.txt", "r") as arquiv:
        saves=arquiv.read()
        label_res.config(text=saves)

def salvar_nome_podio_R():
    with open("PodioR.txt", "r") as arquiv:
        saves=arquiv.read()
        label_ress.config(text=saves)

def juntos_N():
    salvar_nomeN()
    salvar_nome_podio_N()
    mostrar_tela(tela_pergun1N)

def juntos_R():
    salvar_nomeR()
    salvar_nome_podio_R()

def perg():
    with open("perguntas_nutella.txt", "r", encoding="UTF-8") as pop:
        linha = pop.readlines()
    print(linha)


#pontos = 0
#user = ""
#dificuldade = ""
# Janela principal

janela = tk.Tk()
janela.title("QUIZINHO")
janela.geometry("405x530")

# ========== TELA MENU ==========
tela1 = tk.Frame(janela)
enquadramento(0, 0)
titulo = tk.Label(tela1, text="🎮QUIZINHO🎮", font=("Segoe UI Emoji", 40), bg="#0ca5f7", fg="white")
titulo.grid(column=0, row=1, pady=10)
enquadramento(0, 2)
titulo2 = tk.Label(tela1, text="😎Bem-vindo ao Quizinho😎", font=("Segoe UI Emoji", 20))
titulo2.grid(column=0, row=3, pady=10)
bot_comecar = Button(tela1, text="* COMEÇAR JOGO *", font=("Terminal", 20),bg="blue", fg="white",width=20, height=2, command=lambda: mostrar_tela(tela_jogo))
bot_comecar.grid(column=0, row=4, pady=10)
bot_podio = Button(tela1, text="* PÓDIO ATUAL *", font=("Terminal", 20), bg="blue", fg="white",width=20, height=2, command=lambda: mostrar_tela(tela_podio))
bot_podio.grid(column=0, row=5, pady=10)
bot_sair = Button(tela1, text="* SAIR *", font=("Terminal", 20), bg="blue", fg="white",width=20, height=2, command=janela.quit)
bot_sair.grid(column=0, row=6, pady=10)
tela1.pack(fill="both", expand=True)

# ========== TELA JOGO ==========
tela_jogo = tk.Frame(janela, bg="lightgreen")
titulo_jogo = tk.Label(tela_jogo, text="Digite seu nome:", font=("Terminal", 20), bg="lightgreen")
titulo_jogo.place(x=16, y=20)
entrada_nome = tk.Entry(tela_jogo, font=("Terminal", 16), width=15)
entrada_nome.place(x=190,y=25)
esc_dificul = tk.Label(tela_jogo, text="Escolha a Dificuldade:", font=("Terminal", 20), bg="lightgreen")
esc_dificul.place(x=16, y=50)
botaonutella = tk.Button(tela_jogo, text="Nivel Nutella", font=("Terminal", 16), command=lambda:juntos_N())
botaonutella.place(x=16, y=80)
botaoraiz = tk.Button(tela_jogo, text="Nivel Raiz", font=("Terminal", 16), command=lambda:juntos_R())
botaoraiz.place(x=200, y=80)
botao_voltar = tk.Button(tela_jogo, text="↩️ Voltar ao Menu Principal", font=("Segoe UI Emoji", 16),command=lambda: mostrar_tela(tela1))
botao_voltar.place(x=16,y=200)

# ========= TELA PODIO ==========
tela_podio = tk.Frame(janela, bg="#f8ccff")
titulo_pod = tk.Label(tela_podio, text="NIVEL NUTELLA", font=("Terminal", 20), bg="blue", fg="white", width=15, height=1)
titulo_pod.place(x=16, y=20)
titulo_pod2 = tk.Label(tela_podio, text="NIVEL RAIZ", font=("Terminal", 20), bg="blue", fg="white", width=15, height=1)
titulo_pod2.place(x=230, y=20)
label_res=tk.Label(tela_podio, text="", font=("Arial", 15), bg="#f8ccff", fg="black")
label_res.place(x=16, y=50)
label_ress=tk.Label(tela_podio, text="", font=("Arial", 15), bg="#f8ccff", fg="black" )
label_ress.place(x=230, y=50)

# /=/=/=/=/=/=/=/=/=/=/=/=/=/=/ Tela_pergun1N \=\=\=\=\=\=\=\=\=\=\=\=\=\ #

tela_pergun1N = tk.Frame(janela, bg="lightyellow")






botao_voltar = tk.Button(tela_podio, text=" ↩️ Voltar ao Menu Principal", font=("Segoe UI Emoji", 16),command=lambda: mostrar_tela(tela1))
botao_voltar.place(x=66, y=470)

# ========== LOOP PRINCIPAL ==========
janela.mainloop()
