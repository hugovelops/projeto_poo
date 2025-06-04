import sqlite3  # Importa o módulo para trabalhar com banco de dados SQLite

def criar_tabela_e_inserir():
    # Conecta ao banco de dados 'quiz.db'. Se não existir, ele será criado automaticamente.
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

    # Cria a tabela 'perguntas' caso ela ainda não exista
    # A tabela terá as colunas: id (chave primária autoincrementada), enunciado, 4 opções de resposta, e a resposta correta
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enunciado TEXT NOT NULL,
            opcao1 TEXT NOT NULL,
            opcao2 TEXT NOT NULL,
            opcao3 TEXT NOT NULL,
            opcao4 TEXT NOT NULL,
            resposta_correta INTEGER NOT NULL
        )
    """)

    # Lista de perguntas para inserir na tabela
    # Cada tupla contém: enunciado, opção1, opção2, opção3, opção4 e o índice da resposta correta (1 a 4)
    perguntas = [
        ("Qual é o maior oceano do mundo?", "Atlântico", "Índico", "Ártico", "Pacífico", 4),
        ("Quem foi o primeiro homem a pisar na Lua?", "Yuri Gagarin", "Buzz Aldrin", "Neil Armstrong", "Michael Collins", 3),
        ("Qual a capital da Austrália?", "Sydney", "Melbourne", "Canberra", "Brisbane", 3),
        ("Qual é a fórmula química da água?", "CO2", "H2O", "O2", "NaCl", 2),
        ("Qual planeta é conhecido como o Planeta Vermelho?", "Terra", "Marte", "Júpiter", "Saturno", 2),
        ("Em que ano a Segunda Guerra Mundial terminou?", "1940", "1942", "1945", "1950", 3),
        ("Quem escreveu 'Dom Quixote'?", "Cervantes", "Shakespeare", "Machado de Assis", "Fernando Pessoa", 1),
        ("Qual é a maior floresta tropical do mundo?", "Congo", "Taiga", "Amazônica", "Valdiviana", 3),
        ("Qual é o elemento químico com símbolo 'Fe'?", "Ferro", "Flúor", "Fósforo", "Ferroviário", 1),
        ("Qual é a velocidade da luz?", "300.000 km/s", "150.000 km/s", "299.792 km/s", "1.000 km/s", 3)
    ]

    # Limpa a tabela de perguntas antes de inserir as novas (opcional)
    cursor.execute("DELETE FROM perguntas")

    # Insere todas as perguntas da lista na tabela 'perguntas' usando uma única operação para eficiência
    cursor.executemany("""
        INSERT INTO perguntas (enunciado, opcao1, opcao2, opcao3, opcao4, resposta_correta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, perguntas)

    # Salva as alterações no banco de dados
    conn.commit()

    # Fecha a conexão com o banco
    conn.close()

    # Mensagem para indicar que o processo foi concluído com sucesso
    print("Tabela criada e perguntas inseridas com sucesso!")

# Executa a função apenas se o script for rodado diretamente, não quando importado como módulo
if __name__ == "__main__":
    criar_tabela_e_inserir()
