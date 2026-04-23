import tkinter as tk
import time  # MESTRE: Importamos o módulo 'time' para calcular a pontuação.
import random  # MESTRE: Importamos o módulo 'random' para embaralhar as perguntas.

# --- Variáveis Globais de Estado do Jogo ---
# MESTRE: Usaremos estas variáveis para controlar o estado do jogo.
# É uma forma simples de manter a informação entre as telas.
perguntas_carregadas = []
pergunta_atual_index = 0
pontuacao_total = 0
tempo_inicio_pergunta = 0
nome_jogador_atual = ""
dificuldade_atual = ""


# --- Funções de Gerenciamento de Tela ---

def mostrar_tela(tela_ativa):
    """Esconde todas as outras telas e mostra a tela ativa."""
    # MESTRE: Removi a tela_final que não é mais necessária.
    for tela in [tela_menu, tela_jogo, tela_podio, tela_perguntas]:
        tela.pack_forget()
    tela_ativa.pack(fill="both", expand=True)


# --- Funções de Lógica do Jogo e Arquivos ---

def parse_arquivo_perguntas(caminho_arquivo):
    """
    Lê o arquivo .txt e transforma as perguntas em uma estrutura de dados (lista de dicionários).
    MESTRE: Isso torna o código muito mais limpo e fácil de gerenciar do que ler linhas soltas.
    """
    perguntas = []
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip().split('#PERGUNTA')
            for bloco_pergunta in conteudo:
                if not bloco_pergunta.strip():
                    continue

                linhas = bloco_pergunta.strip().split('\n')
                texto_pergunta = linhas[1].strip()
                opcoes = {
                    'a': linhas[2].strip()[3:],
                    'b': linhas[3].strip()[3:],
                    'c': linhas[4].strip()[3:],
                    'd': linhas[5].strip()[3:],
                }
                resposta_correta = linhas[6].replace('RESPOSTA:', '').strip()

                perguntas.append({
                    'pergunta': texto_pergunta,
                    'opcoes': opcoes,
                    'resposta': resposta_correta
                })
    except FileNotFoundError:
        return None
    except IndexError:
        print(
            f"Erro de formatação no arquivo {caminho_arquivo}. Verifique se todas as perguntas têm 6 linhas + resposta.")
        return None

    return perguntas


def iniciar_jogo(dificuldade):
    """Salva o nome do jogador, carrega as perguntas e inicia o quiz."""
    global nome_jogador_atual, dificuldade_atual, perguntas_carregadas, pergunta_atual_index, pontuacao_total

    nome = entrada_nome.get()
    if not nome:
        feedback_nome.config(text="Por favor, digite um nome!")
        return

    feedback_nome.config(text="")
    nome_jogador_atual = nome
    dificuldade_atual = dificuldade

    arquivo_perguntas = "perguntas_nutella.txt" if dificuldade == "Nutella" else "perguntas_raiz.txt"
    perguntas_raw = parse_arquivo_perguntas(arquivo_perguntas)

    if perguntas_raw is None:
        mostrar_tela(tela_perguntas)
        label_pergunta.config(text=f"Erro: Arquivo '{arquivo_perguntas}' não encontrado ou mal formatado!")
        for btn in botoes_resposta:
            btn.pack_forget()
        return

    random.shuffle(perguntas_raw)
    perguntas_carregadas = perguntas_raw[:10]
    pergunta_atual_index = 0
    pontuacao_total = 0

    mostrar_tela(tela_perguntas)
    mostrar_proxima_pergunta()


def mostrar_proxima_pergunta():
    """Exibe a próxima pergunta ou finaliza o jogo se não houver mais perguntas."""
    global pergunta_atual_index, tempo_inicio_pergunta

    # Garante que os botões de resposta estão visíveis no início de cada pergunta
    for btn in botoes_resposta:
        btn.pack(pady=5, fill='x', padx=50)

    if pergunta_atual_index < len(perguntas_carregadas):
        pergunta_info = perguntas_carregadas[pergunta_atual_index]

        label_pergunta.config(text=f"Pergunta {pergunta_atual_index + 1}/10\n\n{pergunta_info['pergunta']}")

        opcoes = pergunta_info['opcoes']
        botoes_resposta[0].config(text=f"a) {opcoes['a']}", command=lambda: verificar_resposta('a'))
        botoes_resposta[1].config(text=f"b) {opcoes['b']}", command=lambda: verificar_resposta('b'))
        botoes_resposta[2].config(text=f"c) {opcoes['c']}", command=lambda: verificar_resposta('c'))
        botoes_resposta[3].config(text=f"d) {opcoes['d']}", command=lambda: verificar_resposta('d'))

        tempo_inicio_pergunta = time.time()
    else:
        # MESTRE: CORREÇÃO APLICADA AQUI!
        # Fim do jogo - Mostra o resultado e esconde os botões.
        label_pergunta.config(
            text=f"Quiz Finalizado!\n\nParabéns, {nome_jogador_atual}!\nSua pontuação final foi:\n{pontuacao_total} pontos")

        # Esconde os botões de resposta pois o jogo acabou.
        for btn in botoes_resposta:
            btn.pack_forget()

        # Salva o nome e a pontuação no arquivo correspondente
        arquivo_podio = "PodioN.txt" if dificuldade_atual == "Nutella" else "PodioR.txt"
        try:
            with open(arquivo_podio, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"{nome_jogador_atual} - {pontuacao_total} pontos\n")
        except Exception as e:
            print(f"Não foi possível salvar no pódio: {e}")


def verificar_resposta(resposta_usuario):
    """Verifica se a resposta está correta, calcula a pontuação e avança."""
    global pontuacao_total, pergunta_atual_index

    tempo_final_pergunta = time.time()
    tempo_decorrido = tempo_final_pergunta - tempo_inicio_pergunta

    pergunta_info = perguntas_carregadas[pergunta_atual_index]
    resposta_correta = pergunta_info['resposta']

    if resposta_usuario == resposta_correta:
        pontos = int(1000 / max(1, tempo_decorrido))
        pontuacao_total += pontos

    pergunta_atual_index += 1
    mostrar_proxima_pergunta()


def atualizar_e_mostrar_podio():
    """Lê os arquivos de pódio e atualiza os placares antes de mostrar a tela."""

    def ler_podio(arquivo, label):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = [linha.strip() for linha in f.readlines() if linha.strip()]
                try:
                    linhas_ordenadas = sorted(linhas, key=lambda x: int(x.split(' - ')[1].split(' ')[0]), reverse=True)
                    saves = "\n".join(linhas_ordenadas)
                except (IndexError, ValueError):
                    saves = "\n".join(linhas)

                label.config(text=saves or "Ninguém jogou ainda.")
        except FileNotFoundError:
            label.config(text=f"Pódio ainda não existe.")

    ler_podio("PodioN.txt", label_res_n)
    ler_podio("PodioR.txt", label_res_r)

    mostrar_tela(tela_podio)


# --- Configuração da Interface Gráfica (Janela Principal) ---
janela = tk.Tk()
janela.title("QUIZINHO DO MESTRE")
janela.geometry("420x550")
janela.configure(bg="#f0f0f0")

# --- Telas (Frames) ---
tela_menu = tk.Frame(janela, bg="#e0e0e0")
tela_jogo = tk.Frame(janela, bg="#d6f9d6")
tela_podio = tk.Frame(janela, bg="#f8e0ff")
tela_perguntas = tk.Frame(janela, bg="#fffacd")

# ========== TELA MENU ==========
titulo = tk.Label(tela_menu, text="🎮 QUIZINHO 🎮", font=("Segoe UI Emoji", 40), bg="#0ca5f7", fg="white", pady=10)
titulo.pack(fill="x")
titulo2 = tk.Label(tela_menu, text="😎 Bem-vindo, Discípulo 😎", font=("Segoe UI Emoji", 20), bg=tela_menu.cget('bg'))
titulo2.pack(pady=20)
bot_comecar = tk.Button(tela_menu, text="* COMEÇAR JOGO *", font=("Terminal", 20), bg="blue", fg="white", width=20,
                        height=2, command=lambda: mostrar_tela(tela_jogo))
bot_comecar.pack(pady=10)
bot_podio = tk.Button(tela_menu, text="* PÓDIO ATUAL *", font=("Terminal", 20), bg="blue", fg="white", width=20,
                      height=2,
                      command=atualizar_e_mostrar_podio)
bot_podio.pack(pady=10)
bot_sair = tk.Button(tela_menu, text="* SAIR *", font=("Terminal", 20), bg="blue", fg="white", width=20, height=2,
                     command=janela.quit)
bot_sair.pack(pady=10)

# ========== TELA JOGO (Escolha de Dificuldade) ==========
titulo_jogo = tk.Label(tela_jogo, text="Digite seu nome:", font=("Terminal", 20), bg=tela_jogo.cget('bg'))
titulo_jogo.pack(pady=(20, 5))
entrada_nome = tk.Entry(tela_jogo, font=("Terminal", 16), width=20, justify='center')
entrada_nome.pack(pady=5)
feedback_nome = tk.Label(tela_jogo, text="", font=("Terminal", 12), fg="red", bg=tela_jogo.cget('bg'))
feedback_nome.pack()
esc_dificul = tk.Label(tela_jogo, text="Escolha a Dificuldade:", font=("Terminal", 20), bg=tela_jogo.cget('bg'))
esc_dificul.pack(pady=(20, 10))
botaonutella = tk.Button(tela_jogo, text="Nível Nutella", font=("Terminal", 16),
                         command=lambda: iniciar_jogo("Nutella"))
botaonutella.pack(pady=10)
botaoraiz = tk.Button(tela_jogo, text="Nível Raiz", font=("Terminal", 16), command=lambda: iniciar_jogo("Raiz"))
botaoraiz.pack(pady=10)
botao_voltar_jogo = tk.Button(tela_jogo, text="↩ Voltar ao Menu", font=("Segoe UI Emoji", 16),
                              command=lambda: mostrar_tela(tela_menu))
botao_voltar_jogo.pack(pady=50)

# ========== TELA PÓDIO ==========
frame_podios = tk.Frame(tela_podio, bg=tela_podio.cget('bg'))
frame_podio_n = tk.Frame(frame_podios, bg=tela_podio.cget('bg'), relief="sunken", borderwidth=2)
frame_podio_r = tk.Frame(frame_podios, bg=tela_podio.cget('bg'), relief="sunken", borderwidth=2)

titulo_pod_n = tk.Label(frame_podio_n, text="NÍVEL NUTELLA", font=("Terminal", 16), bg="blue", fg="white")
titulo_pod_n.pack(pady=5, padx=10, fill="x")
label_res_n = tk.Label(frame_podio_n, text="", font=("Arial", 12), bg="#f8e0ff", fg="black", justify="left",
                       wraplength=180, height=15)
label_res_n.pack(pady=5, padx=10)

titulo_pod_r = tk.Label(frame_podio_r, text="NÍVEL RAIZ", font=("Terminal", 16), bg="red", fg="white")
titulo_pod_r.pack(pady=5, padx=10, fill="x")
label_res_r = tk.Label(frame_podio_r, text="", font=("Arial", 12), bg="#f8e0ff", fg="black", justify="left",
                       wraplength=180, height=15)
label_res_r.pack(pady=5, padx=10)

frame_podio_n.pack(side="left", padx=10, pady=20, fill="both", expand=True)
frame_podio_r.pack(side="right", padx=10, pady=20, fill="both", expand=True)
frame_podios.pack(fill="both", expand=True)

botao_voltar_podio = tk.Button(tela_podio, text="↩ Voltar ao Menu", font=("Segoe UI Emoji", 16),
                               command=lambda: mostrar_tela(tela_menu))
botao_voltar_podio.pack(pady=20)

# ========== TELA DE PERGUNTAS ==========
label_pergunta = tk.Label(tela_perguntas, text="A pergunta aparecerá aqui...", font=("Terminal", 14), wraplength=380,
                          bg=tela_perguntas.cget('bg'), justify="center")
label_pergunta.pack(pady=30, padx=20)

frame_respostas = tk.Frame(tela_perguntas, bg=tela_perguntas.cget('bg'))
frame_respostas.pack(pady=10, fill='x')

botoes_resposta = []
for i in range(4):
    botao = tk.Button(frame_respostas, font=("Terminal", 12), width=30)
    botao.pack(pady=5, fill='x', padx=50)
    botoes_resposta.append(botao)

botao_desistir_perg = tk.Button(tela_perguntas, text="↩ Voltar ao Menu", font=("Segoe UI Emoji", 16),
                                command=lambda: mostrar_tela(tela_menu))
botao_desistir_perg.pack(pady=40)

# --- Inicialização ---
mostrar_tela(tela_menu)
janela.mainloop()
