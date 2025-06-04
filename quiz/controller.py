
from database import Database
from models import Pergunta


class Controller:
    def __init__(self):
        self.db = Database()
        self.perguntas = self.db.carregar_perguntas()
        self.indice_atual = -1
        self.pontuacao = 0

    def get_proxima_pergunta(self):
        if self.indice_atual < len(self.perguntas):
            return self.perguntas[self.indice_atual]
        return None

    def verificar_resposta(self, indice):
        pergunta = self.perguntas[self.indice_atual]
        correta = pergunta.resposta_correta
        self.indice_atual += 1
        if indice == correta:
            self.pontuacao += 1
            return True
        return False

    def reiniciar(self):
        self.indice_atual = 0
        self.pontuacao = 0
