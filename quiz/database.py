import sqlite3

class PerguntaBanco:
    def __init__(self, enunciado, opcao1, opcao2, opcao3, opcao4, resposta_correta, dificuldade):
        self.enunciado = enunciado
        self.opcoes = [opcao1, opcao2, opcao3, opcao4]
        self.resposta_correta = resposta_correta
        self.dificuldade = dificuldade

class Database:
    def __init__(self):
        # Apaga o banco antigo para garantir banco limpo (CUIDADO: apaga tudo)
        import os
        if os.path.exists("quiz.db"):
            os.remove("quiz.db")

        self.conn = sqlite3.connect("quiz.db")
        self.cursor = self.conn.cursor()
        self.criar_tabela()
        self.inserir_perguntas_exemplo()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enunciado TEXT NOT NULL,
                opcao1 TEXT NOT NULL,
                opcao2 TEXT NOT NULL,
                opcao3 TEXT NOT NULL,
                opcao4 TEXT NOT NULL,
                resposta_correta INTEGER NOT NULL,
                dificuldade TEXT
            )
        """)
        self.conn.commit()

    def inserir_perguntas_exemplo(self):
        perguntas = [
            ("Qual é a capital do Brasil?", "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", 3, "Fácil"),
            ("Quem escreveu 'Dom Casmurro'?", "Machado de Assis", "Carlos Drummond", "Clarice Lispector", "Monteiro Lobato", 1, "Média"),
            ("Quanto é 7 x 8?", "54", "56", "58", "60", 2, "Fácil"),
            ("Qual é a fórmula da água?", "H2O", "CO2", "O2", "NaCl", 1, "Fácil"),
            ("Quem pintou a Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo", 3, "Média"),
            ("Qual o maior planeta do Sistema Solar?", "Terra", "Júpiter", "Saturno", "Marte", 2, "Fácil"),
            ("Em que ano o Brasil foi descoberto?", "1500", "1600", "1400", "1700", 1, "Média"),
            ("Qual elemento químico tem símbolo Fe?", "Ferro", "Flúor", "Fósforo", "Frâncio", 1, "Fácil"),
            ("Quem foi o primeiro presidente do Brasil?", "Getúlio Vargas", "Deodoro da Fonseca", "Juscelino Kubitschek", "Dom Pedro II", 2, "Difícil"),
            ("Qual linguagem de programação é conhecida como 'a linguagem da web'?", "Python", "Java", "JavaScript", "C++", 3, "Fácil")
        ]
        for pergunta in perguntas:
            self.cursor.execute("""
                INSERT INTO perguntas (enunciado, opcao1, opcao2, opcao3, opcao4, resposta_correta, dificuldade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, pergunta)
        self.conn.commit()

    def carregar_perguntas(self):
        self.cursor.execute("SELECT enunciado, opcao1, opcao2, opcao3, opcao4, resposta_correta, dificuldade FROM perguntas")
        dados = self.cursor.fetchall()
        perguntas = []
        for linha in dados:
            pergunta = PerguntaBanco(*linha)
            perguntas.append(pergunta)
        return perguntas
