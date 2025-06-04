class Pergunta:
    def __init__(self, enunciado, opcoes, resposta_correta):
        self.enunciado = enunciado
        self.opcoes = opcoes  # Lista: ["A", "B", "C", "D"]
        self.resposta_correta = resposta_correta  # Índice correto (0, 1, 2, 3)
