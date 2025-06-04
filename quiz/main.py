import tkinter as tk
from tkinter import messagebox, font, scrolledtext
import random
from database import Database  # Importa a classe Database para carregar as perguntas


class Pergunta:
    def __init__(self, enunciado, opcoes, resposta_correta):
        # Inicializa a pergunta com enunciado, opções e índice da resposta correta (1 a 4)
        self.enunciado = enunciado
        self.opcoes_originais = opcoes  # Opções originais na ordem do banco
        self.resposta_correta_texto = opcoes[resposta_correta - 1]  # Texto da resposta correta
        self.opcoes = []  # Opções que serão embaralhadas
        self.resposta_correta = 0  # Novo índice da resposta correta após embaralhar
        self.embaralhar_opcoes()

    def embaralhar_opcoes(self):
        # Embaralha as opções mantendo o controle do índice correto
        opcoes_com_indice = list(enumerate(self.opcoes_originais, start=1))
        random.shuffle(opcoes_com_indice)
        self.opcoes = [texto for _, texto in opcoes_com_indice]
        for novo_indice, (indice_antigo, texto) in enumerate(opcoes_com_indice, start=1):
            if texto == self.resposta_correta_texto:
                self.resposta_correta = novo_indice


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🎓 Quiz Interativo")  # Título da janela
        self.master.geometry("800x600")  # Tamanho da janela
        self.master.configure(bg="#e6f2ff")  # Cor de fundo da janela

        # Definição de fontes personalizadas para título e opções
        self.custom_font = font.Font(family="Comic Sans MS", size=14)
        self.title_font = font.Font(family="Comic Sans MS", size=20, weight="bold")

        self.db = Database()  # Instancia o banco de dados
        perguntas_raw = self.db.carregar_perguntas()  # Carrega perguntas do banco

        # Cria objetos Pergunta e embaralha a lista para ordem aleatória
        self.perguntas = [Pergunta(p.enunciado, p.opcoes, p.resposta_correta) for p in perguntas_raw]
        random.shuffle(self.perguntas)

        # Variáveis de controle do quiz
        self.indice_pergunta = 0
        self.pontuacao = 0
        self.erros = []  # Guarda perguntas e respostas erradas

        # Frame central que contém o card do quiz
        self.card = tk.Frame(self.master, bg="#ffffff",
                             padx=30, pady=30, relief="groove", borderwidth=3)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # Label para mostrar o enunciado da pergunta
        self.label_pergunta = tk.Label(
            self.card, text="", wraplength=650, font=self.title_font,
            bg="#ffffff", fg="#333333", justify="left"
        )
        self.label_pergunta.pack(pady=(0, 20))

        # Variável para armazenar a resposta selecionada
        self.var_resposta = tk.IntVar()
        self.botoes_resposta = []
        for i in range(4):
            # Cria 4 botões do tipo Radiobutton para as opções
            btn = tk.Radiobutton(
                self.card, text="", variable=self.var_resposta,
                value=i + 1, font=self.custom_font,
                bg="#d9f0ff", fg="#003366", selectcolor="#99ccff",
                activebackground="#b3d1ff", activeforeground="#003366",
                anchor="w", padx=10, indicatoron=False, width=50, relief="raised"
            )
            btn.pack(fill="x", pady=6)
            # Efeitos visuais ao passar o mouse sobre o botão
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#99ccff"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#d9f0ff"))
            self.botoes_resposta.append(btn)

        # Botão para confirmar a resposta escolhida
        self.botao_confirmar = tk.Button(
            self.card, text="✅ Confirmar", font=self.custom_font,
            command=self.confirmar_resposta, bg="#3399ff", fg="#ffffff",
            activebackground="#267acc", width=20
        )
        self.botao_confirmar.pack(pady=(20, 10))

        # Botão para reiniciar o quiz, inicialmente desabilitado
        self.botao_reiniciar = tk.Button(
            self.card, text="🔁 Recomeçar", font=self.custom_font,
            command=self.reiniciar_quiz, bg="#33cc33", fg="#ffffff",
            activebackground="#28a428", width=20
        )
        self.botao_reiniciar.pack()
        self.botao_reiniciar.config(state="disabled")

        # Exibe a primeira pergunta ao iniciar o programa
        self.exibir_pergunta()

    def exibir_pergunta(self):
        # Exibe a pergunta atual e suas opções
        if self.indice_pergunta < len(self.perguntas):
            pergunta = self.perguntas[self.indice_pergunta]
            self.label_pergunta.config(text=f"📘 {pergunta.enunciado}")
            for i, opcao in enumerate(pergunta.opcoes):
                self.botoes_resposta[i].config(text=f"• {opcao}")
            self.var_resposta.set(0)  # Limpa seleção anterior
        else:
            # Se acabar as perguntas, finaliza o quiz
            self.finalizar_quiz()

    def confirmar_resposta(self):
        # Captura a resposta selecionada pelo usuário
        selecionado = self.var_resposta.get()
        if selecionado == 0:
            # Se não selecionar nenhuma opção, avisa o usuário
            messagebox.showwarning(
                "⚠️ Atenção", "Escolha uma opção antes de confirmar!")
            return
        pergunta = self.perguntas[self.indice_pergunta]
        if selecionado == pergunta.resposta_correta:
            # Incrementa pontuação se acertar
            self.pontuacao += 1
        else:
            # Salva a pergunta e resposta errada para mostrar depois
            self.erros.append((pergunta, selecionado))
        self.indice_pergunta += 1  # Passa para a próxima pergunta
        self.exibir_pergunta()

    def finalizar_quiz(self):
        # Exibe resultado final no label e desabilita botões de resposta
        resultado = f"🎉 Quiz Finalizado!\n\n🎯 Sua pontuação: {self.pontuacao} de {len(self.perguntas)}"
        self.label_pergunta.config(text=resultado)
        for rb in self.botoes_resposta:
            rb.pack_forget()  # Remove botões de opções da tela
        self.botao_confirmar.config(state="disabled")
        self.botao_reiniciar.config(state="normal")

        # Mensagens de acordo com o desempenho
        if self.pontuacao == len(self.perguntas):
            messagebox.showinfo(
                "Parabéns!", "🏆 Você acertou todas! Mestre do conhecimento!")
        elif self.pontuacao >= len(self.perguntas) // 2:
            messagebox.showinfo(
                "Muito bem!", "👏 Bom trabalho! Continue estudando!")
        else:
            messagebox.showinfo(
                "Tente de novo", "❌ Não desista, tente novamente!")

        # Se houver erros, mostra a janela com as perguntas erradas
        if self.erros:
            self.mostrar_erros_janela()

    def mostrar_erros_janela(self):
        # Cria uma nova janela para mostrar as perguntas erradas
        janela_erros = tk.Toplevel(self.master)
        janela_erros.title("Perguntas que você errou")
        janela_erros.geometry("700x500")
        janela_erros.configure(bg="#f9f9f9")

        # Título da janela de erros
        titulo = tk.Label(janela_erros, text="Perguntas Erradas",
                          font=("Comic Sans MS", 20, "bold"),
                          bg="#f9f9f9", fg="#cc0000")
        titulo.pack(pady=15)

        # Caixa de texto com barra de rolagem para exibir detalhes dos erros
        texto = scrolledtext.ScrolledText(janela_erros, font=("Comic Sans MS", 12),
                                         bg="#ffffff", fg="#000000")
        texto.pack(padx=15, pady=10, fill="both", expand=True)

        # Insere cada pergunta errada com sua resposta e a correta
        for i, (p, r) in enumerate(self.erros, start=1):
            texto.insert(tk.END, f"{i}. Pergunta:\n{p.enunciado}\n")
            texto.insert(tk.END, f"Sua resposta: {p.opcoes[r - 1]}\n")
            texto.insert(tk.END, f"Resposta correta: {p.opcoes[p.resposta_correta - 1]}\n")
            texto.insert(tk.END, "-" * 60 + "\n")

        texto.config(state="disabled")  # Torna o texto somente leitura

    def reiniciar_quiz(self):
        # Reseta variáveis para reiniciar o quiz e exibe a primeira pergunta
        self.indice_pergunta = 0
        self.pontuacao = 0
        self.erros = []
        for rb in self.botoes_resposta:
            rb.pack()  # Reexibe os botões de opção
        self.botao_confirmar.config(state="normal")
        self.botao_reiniciar.config(state="disabled")
        self.exibir_pergunta()


if __name__ == "__main__":
    # Inicializa o Tkinter e executa o quiz
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
