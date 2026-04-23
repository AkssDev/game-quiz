import tkinter as tk
from tkinter import Button


def enquadramento(m, n):
    label = tk.Label(tela1, text="=" * 13, font=("Terminal", 30), bg="blue", fg="white")
    label.grid(column=m, row=n, pady=5)


def mostrar_tela(tela):
    for frame in [tela1, tela_jogo, tela_podio, tela_quiz]:
        frame.pack_forget()
    tela.pack(fill="both", expand=True)

    # Centralizar a tela
    if tela == tela_quiz:
        tela.pack(fill="both", expand=True)
        # Reabilitar botões quando voltar ao quiz
        for botao in [botao_a, botao_b, botao_c, botao_d]:
            botao.config(state="normal")
        botao_reiniciar.config(state="disabled")
        resultado_label.config(text="")


def salvar_nomeN():
    nome = entrada_nome.get()
    if nome.strip():  # Verificar se nome não está vazio
        with open("PodioN.txt", "a") as arquivo:
            arquivo.write(f"{nome} - {pontos} pontos\n")


def salvar_nomeR():
    nome = entrada_nome.get()
    if nome.strip():  # Verificar se nome não está vazio
        with open("PodioR.txt", "a") as arquivo:
            arquivo.write(f"{nome} - {pontos} pontos\n")


def salvar_nome_podio_N():
    try:
        with open("PodioN.txt", "r") as arquiv:
            saves = arquiv.read()
            label_res.config(text=saves if saves else "Nenhum jogador ainda")
    except FileNotFoundError:
        label_res.config(text="Nenhum jogador ainda")


def salvar_nome_podio_R():
    try:
        with open("PodioR.txt", "r") as arquiv:
            saves = arquiv.read()
            label_ress.config(text=saves if saves else "Nenhum jogador ainda")
    except FileNotFoundError:
        label_ress.config(text="Nenhum jogador ainda")


# Variáveis globais para controle do quiz
pergunta_atual = 0
pontos = 0
perguntas_quiz = []
respostas_corretas = []
tipo_quiz = ""


def carregar_perguntas_nutella():
    try:
        with open("perguntas_nutella.txt", "r", encoding="UTF-8") as arquivo:
            linhas = arquivo.readlines()

        perguntas = []
        respostas = []
        pergunta_temp = ""

        for linha in linhas:
            linha = linha.strip()
            if linha and linha[0].isdigit() and '.' in linha:  # Melhor detecção de início de pergunta
                if pergunta_temp:
                    perguntas.append(pergunta_temp)
                pergunta_temp = linha
            elif linha.startswith(("a)", "b)", "c)", "d)")):
                if pergunta_temp:
                    pergunta_temp += "\n" + linha
            elif linha.startswith("Resposta:"):
                resposta = linha.replace("Resposta: ", "").strip()
                respostas.append(resposta)

        if pergunta_temp:
            perguntas.append(pergunta_temp)

        return perguntas, respostas
    except FileNotFoundError:
        print("Arquivo perguntas_nutella.txt não encontrado")
        return ["1. Qual é a capital do Brasil?\na) São Paulo\nb) Rio de Janeiro\nc) Brasília\nd) Salvador"], [
            "c) Brasília"]


def carregar_perguntas_raiz():
    try:
        with open("perguntas_raiz.txt", "r", encoding="UTF-8") as arquivo:
            linhas = arquivo.readlines()

        perguntas = []
        respostas = []
        pergunta_temp = ""

        for linha in linhas:
            linha = linha.strip()
            if linha and linha[0].isdigit() and '.' in linha:  # Melhor detecção de início de pergunta
                if pergunta_temp:
                    perguntas.append(pergunta_temp)
                pergunta_temp = linha
            elif linha.startswith(("a)", "b)", "c)", "d)")):
                if pergunta_temp:
                    pergunta_temp += "\n" + linha
            elif linha.startswith("Resposta:"):
                resposta = linha.replace("Resposta: ", "").strip()
                respostas.append(resposta)

        if pergunta_temp:
            perguntas.append(pergunta_temp)

        return perguntas, respostas
    except FileNotFoundError:
        print("Arquivo perguntas_raiz.txt não encontrado")
        return ["1. Qual é a raiz quadrada de 144?\na) 10\nb) 12\nc) 14\nd) 16"], ["b) 12"]


def iniciar_quiz_nutella():
    global pergunta_atual, pontos, perguntas_quiz, respostas_corretas, tipo_quiz
    pergunta_atual = 0
    pontos = 0
    tipo_quiz = "nutella"
    perguntas_quiz, respostas_corretas = carregar_perguntas_nutella()
    mostrar_pergunta_atual()


def iniciar_quiz_raiz():
    global pergunta_atual, pontos, perguntas_quiz, respostas_corretas, tipo_quiz
    pergunta_atual = 0
    pontos = 0
    tipo_quiz = "raiz"
    perguntas_quiz, respostas_corretas = carregar_perguntas_raiz()
    mostrar_pergunta_atual()


def mostrar_pergunta_atual():
    if pergunta_atual < len(perguntas_quiz):
        pergunta_text = perguntas_quiz[pergunta_atual]
        linhas = pergunta_text.split('\n')

        # Primeira linha é a pergunta
        pergunta_titulo = linhas[0] if linhas else "Pergunta não encontrada"
        pergunta_label_quiz.config(text=pergunta_titulo)

        # Extrair e configurar as alternativas
        alternativas = {"a": "Opção A", "b": "Opção B", "c": "Opção C", "d": "Opção D"}

        for linha in linhas[1:]:
            if linha.startswith("a)"):
                alternativas["a"] = linha[2:].strip()
            elif linha.startswith("b)"):
                alternativas["b"] = linha[2:].strip()
            elif linha.startswith("c)"):
                alternativas["c"] = linha[2:].strip()
            elif linha.startswith("d)"):
                alternativas["d"] = linha[2:].strip()

        # Configurar botões com texto completo
        botao_a.config(text=alternativas["a"])
        botao_b.config(text=alternativas["b"])
        botao_c.config(text=alternativas["c"])
        botao_d.config(text=alternativas["d"])

        # Atualizar informações do quiz
        pontos_label.config(text=f"Pontos: {pontos}")
        progresso_label.config(text=f"Pergunta {pergunta_atual + 1} de {len(perguntas_quiz)}")

        # Limpar resultado anterior
        resultado_label.config(text="")

        # Reabilitar botões
        for botao in [botao_a, botao_b, botao_c, botao_d]:
            botao.config(state="normal")
    else:
        finalizar_quiz()


def verificar_resposta(resposta_escolhida):
    global pergunta_atual, pontos

    if pergunta_atual >= len(respostas_corretas):
        return

    # Desabilitar botões para evitar múltiplas respostas
    for botao in [botao_a, botao_b, botao_c, botao_d]:
        botao.config(state="disabled")

    # Comparar resposta
    resposta_correta = respostas_corretas[pergunta_atual].strip()

    # Verificar se a resposta está correta
    if resposta_correta.startswith(resposta_escolhida):
        pontos += 1
        resultado_label.config(text="✅ Correto!", fg="green")
    else:
        resultado_label.config(text=f"❌ Errado! Resposta correta: {resposta_correta}", fg="red")

    pergunta_atual += 1

    # Agendar próxima pergunta após 2 segundos
    if pergunta_atual < len(perguntas_quiz):
        janela.after(2000, mostrar_pergunta_atual)
    else:
        janela.after(2000, finalizar_quiz)


def finalizar_quiz():
    global pontos

    # Salvar pontuação no arquivo apropriado
    if tipo_quiz == "nutella":
        salvar_nomeN()
    else:
        salvar_nomeR()

    # Mostrar resultado final
    pergunta_label_quiz.config(text=f"🎉 Quiz finalizado!\n\nSua pontuação: {pontos}/{len(perguntas_quiz)}")

    # Limpar botões
    for botao in [botao_a, botao_b, botao_c, botao_d]:
        botao.config(text="", state="disabled")

    # Habilitar botão de reiniciar
    botao_reiniciar.config(state="normal")

    # Limpar resultado
    resultado_label.config(text="")


def juntos_N():
    nome = entrada_nome.get().strip()
    if not nome:
        tk.messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        return
    iniciar_quiz_nutella()
    mostrar_tela(tela_quiz)


def juntos_R():
    nome = entrada_nome.get().strip()
    if not nome:
        tk.messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        return
    iniciar_quiz_raiz()
    mostrar_tela(tela_quiz)


def reiniciar_quiz():
    if tipo_quiz == "nutella":
        iniciar_quiz_nutella()
    else:
        iniciar_quiz_raiz()


# Janela principal
janela = tk.Tk()
janela.title("QUIZINHO")
janela.geometry("800x600")  # Aumentar tamanho da janela
janela.resizable(False, False)

# ========== TELA MENU ==========
tela1 = tk.Frame(janela, bg="lightblue")
tela1.grid_rowconfigure(0, weight=1)
tela1.grid_rowconfigure(1, weight=1)
tela1.grid_rowconfigure(2, weight=1)
tela1.grid_rowconfigure(3, weight=1)
tela1.grid_rowconfigure(4, weight=1)
tela1.grid_rowconfigure(5, weight=1)
tela1.grid_rowconfigure(6, weight=1)
tela1.grid_columnconfigure(0, weight=1)

enquadramento(0, 0)
titulo = tk.Label(tela1, text="🎮QUIZINHO🎮", font=("Segoe UI Emoji", 40), bg="#0ca5f7", fg="white")
titulo.grid(column=0, row=1, pady=10)
enquadramento(0, 2)
titulo2 = tk.Label(tela1, text="😎Bem-vindo ao Quizinho😎", font=("Segoe UI Emoji", 20), bg="lightblue")
titulo2.grid(column=0, row=3, pady=10)
bot_comecar = Button(tela1, text="* COMEÇAR JOGO *", font=("Terminal", 20), bg="blue", fg="white", width=20, height=2,
                     command=lambda: mostrar_tela(tela_jogo))
bot_comecar.grid(column=0, row=4, pady=10)
bot_podio = Button(tela1, text="* PÓDIO ATUAL *", font=("Terminal", 20), bg="blue", fg="white", width=20, height=2,
                   command=lambda: mostrar_tela(tela_podio))
bot_podio.grid(column=0, row=5, pady=10)
bot_sair = Button(tela1, text="* SAIR *", font=("Terminal", 20), bg="blue", fg="white", width=20, height=2,
                  command=janela.quit)
bot_sair.grid(column=0, row=6, pady=10)

# ========== TELA JOGO ==========
tela_jogo = tk.Frame(janela, bg="lightgreen")
tela_jogo.pack_propagate(False)

# Centralizar elementos
frame_jogo = tk.Frame(tela_jogo, bg="lightgreen")
frame_jogo.pack(expand=True)

titulo_jogo = tk.Label(frame_jogo, text="Digite seu nome:", font=("Terminal", 20), bg="lightgreen")
titulo_jogo.pack(pady=10)

entrada_nome = tk.Entry(frame_jogo, font=("Terminal", 16), width=15)
entrada_nome.pack(pady=5)

esc_dificul = tk.Label(frame_jogo, text="Escolha a Dificuldade:", font=("Terminal", 20), bg="lightgreen")
esc_dificul.pack(pady=10)

frame_botoes_dif = tk.Frame(frame_jogo, bg="lightgreen")
frame_botoes_dif.pack(pady=10)

botaonutella = tk.Button(frame_botoes_dif, text="Nivel Nutella", font=("Terminal", 16), command=juntos_N)
botaonutella.pack(side="left", padx=10)

botaoraiz = tk.Button(frame_botoes_dif, text="Nivel Raiz", font=("Terminal", 16), command=juntos_R)
botaoraiz.pack(side="left", padx=10)

botao_voltar = tk.Button(frame_jogo, text="↩ Voltar ao Menu Principal", font=("Segoe UI Emoji", 16),
                         command=lambda: mostrar_tela(tela1))
botao_voltar.pack(pady=20)

# ========= TELA PODIO ==========
tela_podio = tk.Frame(janela, bg="#f8ccff")

frame_podio = tk.Frame(tela_podio, bg="#f8ccff")
frame_podio.pack(expand=True, fill="both", padx=20, pady=20)

titulo_pod = tk.Label(frame_podio, text="NIVEL NUTELLA", font=("Terminal", 20), bg="blue", fg="white")
titulo_pod.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

titulo_pod2 = tk.Label(frame_podio, text="NIVEL RAIZ", font=("Terminal", 20), bg="blue", fg="white")
titulo_pod2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

label_res = tk.Label(frame_podio, text="", font=("Arial", 12), bg="#f8ccff", fg="black", justify="left", anchor="nw")
label_res.grid(row=1, column=0, padx=10, pady=10, sticky="new")

label_ress = tk.Label(frame_podio, text="", font=("Arial", 12), bg="#f8ccff", fg="black", justify="left", anchor="nw")
label_ress.grid(row=1, column=1, padx=10, pady=10, sticky="new")

frame_podio.grid_columnconfigure(0, weight=1)
frame_podio.grid_columnconfigure(1, weight=1)
frame_podio.grid_rowconfigure(1, weight=1)

botao_carregar_podios = tk.Button(frame_podio, text="📊 Carregar Pódios", font=("Segoe UI Emoji", 14),
                                  command=lambda: [salvar_nome_podio_N(), salvar_nome_podio_R()])
botao_carregar_podios.grid(row=2, column=0, columnspan=2, pady=10)

botao_voltar_podio = tk.Button(frame_podio, text="↩ Voltar ao Menu Principal", font=("Segoe UI Emoji", 16),
                               command=lambda: mostrar_tela(tela1))
botao_voltar_podio.grid(row=3, column=0, columnspan=2, pady=10)

# ========== TELA QUIZ INTERATIVO ==========
tela_quiz = tk.Frame(janela, bg="lightblue")

# Container principal centralizado
main_container = tk.Frame(tela_quiz, bg="lightblue")
main_container.pack(expand=True, fill="both", padx=20, pady=20)

# Título
titulo_quiz = tk.Label(main_container, text="🎯 QUIZ INTERATIVO", font=("Terminal", 24), bg="darkblue", fg="white")
titulo_quiz.pack(pady=(0, 20))

# Progresso e pontos
info_frame = tk.Frame(main_container, bg="lightblue")
info_frame.pack(pady=10)

progresso_label = tk.Label(info_frame, text="Pergunta 1 de 10", font=("Arial", 14), bg="lightblue")
progresso_label.pack()

pontos_label = tk.Label(info_frame, text="Pontos: 0", font=("Arial", 14), bg="lightblue", fg="darkblue")
pontos_label.pack()

# Pergunta
pergunta_label_quiz = tk.Label(main_container, text="Carregando pergunta...", font=("Arial", 16), bg="lightblue",
                               wraplength=600, justify="center")
pergunta_label_quiz.pack(pady=20)

# Botões das alternativas
frame_botoes = tk.Frame(main_container, bg="lightblue")
frame_botoes.pack(pady=10)

botao_a = tk.Button(frame_botoes, text="A)", font=("Arial", 12), width=50, bg="white", wraplength=400,
                    command=lambda: verificar_resposta("a)"))
botao_a.pack(pady=5)

botao_b = tk.Button(frame_botoes, text="B)", font=("Arial", 12), width=50, bg="white", wraplength=400,
                    command=lambda: verificar_resposta("b)"))
botao_b.pack(pady=5)

botao_c = tk.Button(frame_botoes, text="C)", font=("Arial", 12), width=50, bg="white", wraplength=400,
                    command=lambda: verificar_resposta("c)"))
botao_c.pack(pady=5)

botao_d = tk.Button(frame_botoes, text="D)", font=("Arial", 12), width=50, bg="white", wraplength=400,
                    command=lambda: verificar_resposta("d)"))
botao_d.pack(pady=5)

# Resultado da resposta
resultado_label = tk.Label(main_container, text="", font=("Arial", 14), bg="lightblue")
resultado_label.pack(pady=10)

# Botões de controle
frame_controle = tk.Frame(main_container, bg="lightblue")
frame_controle.pack(pady=20)

botao_reiniciar = tk.Button(frame_controle, text="🔄 Reiniciar Quiz", font=("Arial", 12), bg="orange", fg="white",
                            state="disabled", command=reiniciar_quiz)
botao_reiniciar.pack(side="left", padx=5)

botao_voltar_quiz = tk.Button(frame_controle, text="↩ Voltar ao Menu", font=("Arial", 12), bg="red", fg="white",
                              command=lambda: mostrar_tela(tela1))
botao_voltar_quiz.pack(side="left", padx=5)

# Iniciar com a tela principal
mostrar_tela(tela1)

# ========== LOOP PRINCIPAL ==========
janela.mainloop()