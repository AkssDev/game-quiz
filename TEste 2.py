import tkinter as tk
from tkinter import messagebox

# ============================ CONFIGURAÇÕES ============================
NUM_PERGUNTAS = 10

# ======================= LEITURA DAS PERGUNTAS ========================
def carregar_perguntas(arquivo):
    perguntas = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.read().strip().split('\n\n')
        for bloco in linhas:
            linhas_blocadas = bloco.strip().split('\n')
            pergunta = linhas_blocadas[0][len('Pergunta: '):]
            alternativas = [linha for linha in linhas_blocadas[1:5]]
            resposta = linhas_blocadas[5][len('Resposta: '):].strip().lower()
            perguntas.append((pergunta, alternativas, resposta))
    return perguntas[:NUM_PERGUNTAS]

# ======================= JANELA PRINCIPAL =============================
janela = tk.Tk()
janela.title("Quizinho")
janela.geometry("500x400")

# ========================= VARIÁVEIS GLOBAIS ==========================
perguntas = []
indice_pergunta = 0
pontuacao = 0
resposta_selecionada = tk.StringVar()
nome_jogador = ""

def iniciar_quiz(arquivo_perguntas, nome):
    global perguntas, indice_pergunta, pontuacao, nome_jogador
    perguntas = carregar_perguntas(arquivo_perguntas)
    indice_pergunta = 0
    pontuacao = 0
    nome_jogador = nome
    mostrar_pergunta()

def mostrar_pergunta():
    global indice_pergunta, resposta_selecionada
    if indice_pergunta < NUM_PERGUNTAS:
        for widget in tela_pergunta.winfo_children():
            widget.destroy()

        pergunta_atual, alternativas, _ = perguntas[indice_pergunta]
        tk.Label(tela_pergunta, text=f"Pergunta {indice_pergunta+1} de {NUM_PERGUNTAS}", font=("Arial", 14)).pack(pady=10)
        tk.Label(tela_pergunta, text=pergunta_atual, font=("Arial", 16)).pack(pady=10)

        resposta_selecionada.set(None)
        for alt in alternativas:
            opcao = alt[0].lower()
            texto = alt
            tk.Radiobutton(tela_pergunta, text=texto, variable=resposta_selecionada, value=opcao, font=("Arial", 14)).pack(anchor='w', padx=30)

        tk.Button(tela_pergunta, text="Próxima", font=("Arial", 14), command=verificar_resposta).pack(pady=20)
        trocar_tela(tela_pergunta)
    else:
        mostrar_resultado()

def verificar_resposta():
    global pontuacao, indice_pergunta
    _, _, resposta_correta = perguntas[indice_pergunta]
    if resposta_selecionada.get() == resposta_correta:
        pontuacao += 1
    indice_pergunta += 1
    mostrar_pergunta()

def mostrar_resultado():
    for widget in tela_resultado.winfo_children():
        widget.destroy()

    tk.Label(tela_resultado, text=f"Parabéns, {nome_jogador}!", font=("Arial", 18)).pack(pady=10)
    tk.Label(tela_resultado, text=f"Sua pontuação: {pontuacao}/{NUM_PERGUNTAS}", font=("Arial", 18)).pack(pady=10)
    tk.Button(tela_resultado, text="Voltar ao Menu", font=("Arial", 14), command=lambda: trocar_tela(tela_menu)).pack(pady=20)
    trocar_tela(tela_resultado)

# ======================== TELAS PRINCIPAIS ============================
tela_menu = tk.Frame(janela)
tela_pergunta = tk.Frame(janela)
tela_resultado = tk.Frame(janela)

def trocar_tela(tela):
    for frame in [tela_menu, tela_pergunta, tela_resultado]:
        frame.pack_forget()
    tela.pack(fill='both', expand=True)

# ======================== CONTEÚDO TELA MENU ==========================
tk.Label(tela_menu, text="QUIZINHO", font=("Arial", 24)).pack(pady=20)
tk.Label(tela_menu, text="Digite seu nome:", font=("Arial", 16)).pack()
nome_entry = tk.Entry(tela_menu, font=("Arial", 16))
nome_entry.pack(pady=10)

tk.Label(tela_menu, text="Escolha a Dificuldade:", font=("Arial", 16)).pack(pady=10)

tk.Button(tela_menu, text="Nivel Nutella", font=("Arial", 16), command=lambda: iniciar_quiz("perguntas_nutella.txt", nome_entry.get())).pack(pady=5)
tk.Button(tela_menu, text="Nivel Raiz", font=("Arial", 16), command=lambda: iniciar_quiz("perguntas_raiz.txt", nome_entry.get())).pack(pady=5)
tk.Button(tela_menu, text="Sair", font=("Arial", 16), command=janela.quit).pack(pady=20)

# ============================= INICIAL ================================
trocar_tela(tela_menu)

janela.mainloop()