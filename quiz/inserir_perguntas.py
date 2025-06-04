import sqlite3  # Importa a biblioteca para manipular banco de dados SQLite

def criar_tabela():
    # Função para criar a tabela 'perguntas' no banco de dados, se ela ainda não existir
    conn = sqlite3.connect("quiz.db")  # Conecta (ou cria) o banco de dados 'quiz.db'
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

    # Executa um comando SQL para criar a tabela 'perguntas' com os seguintes campos:
    # id: identificador único auto-incrementado
    # enunciado: texto da pergunta
    # opcao1 a opcao4: as quatro opções de resposta possíveis
    # resposta_correta: número indicando qual opção é a correta (1 a 4)
    # dificuldade: texto para indicar a dificuldade da pergunta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enunciado TEXT NOT NULL,
            opcao1 TEXT NOT NULL,
            opcao2 TEXT NOT NULL,
            opcao3 TEXT NOT NULL,
            opcao4 TEXT NOT NULL,
            resposta_correta INTEGER NOT NULL,
            dificuldade TEXT NOT NULL
        );
    """)

    conn.commit()  # Salva as alterações feitas no banco
    conn.close()   # Fecha a conexão com o banco de dados

def inserir_perguntas():
    # Função para inserir perguntas na tabela 'perguntas'
    perguntas = [
        # Perguntas fáceis
        ("Qual a capital da França?", "Paris",
        "Londres", "Roma", "Berlim", 1, "Fácil"),
        ("Qual é o valor aproximado de π?", "3.14",
        "2.17", "3.41", "3.15", 1, "Fácil"),

        # Perguntas difíceis
        ("Qual o nome do físico que formulou a Teoria da Relatividade?",
        "Newton", "Einstein", "Galileo", "Tesla", 2, "Difícil"),
        ("Qual o elemento químico com símbolo 'Au'?",
        "Prata", "Ouro", "Ferro", "Mercúrio", 2, "Difícil"),

        # Perguntas impossíveis
        ("Qual a fórmula do ácido sulfúrico?", "HCl",
        "H2SO4", "CO2", "NaOH", 2, "Impossível"),
        ("Quem descobriu a estrutura do DNA?", "Watson",
        "Crick", "Franklin", "Mendel", 3, "Impossível"),
    ]

    conn = sqlite3.connect("quiz.db")  # Abre conexão com o banco 'quiz.db'
    cursor = conn.cursor()  # Cria cursor para executar comandos

    # Insere as perguntas uma a uma na tabela usando parâmetros para evitar injeção de SQL
    for pergunta in perguntas:
        cursor.execute("""
            INSERT INTO perguntas (enunciado, opcao1, opcao2, opcao3, opcao4, resposta_correta, dificuldade)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, pergunta)

    conn.commit()  # Salva as mudanças no banco
    conn.close()   # Fecha a conexão com o banco

# Bloco principal: só executa se o arquivo for rodado diretamente (não importado)
if __name__ == "__main__":
    criar_tabela()        # Cria a tabela perguntas, se ainda não existir
    inserir_perguntas()   # Insere as perguntas no banco
    print("Tabela criada e perguntas inseridas com sucesso!")  # Mensagem de confirmação
