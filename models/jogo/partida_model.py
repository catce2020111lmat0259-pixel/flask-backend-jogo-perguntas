class Partida:
    partidas = []
    id_contar = 1

    def __init__(self, data):
        """
        Inicializa um objeto da classe Partida com os dados da partida.

        Args:
            data (dict): Dicionário com os dados da partida.

        Attributes:
            id (int): Número único da partida.
            data (dict): Dicionário com os dados da partida.
            errors (list): Lista de erros.
            questoes (list): Lista de questões da partida.
            indice (int): Índice da próxima questão a ser respondida.
            perguntas_respondidas (int): Número de perguntas respondidas.
            acertos (int): Número de acertos.
            erros (int): Número de erros.
            questao_atual (Questao): Objeto da classe Questao com a próxima questão a ser respondida.
        """
        self.id = Partida.id_contar
        Partida.id_contar += 1

        self.data = data
        self.errors = []

        self.questoes = data.get('questoes', [])[:]

        self.indice = 0
        self.perguntas_respondidas = data.get('perguntas_respondidas', 0)
        self.acertos = data.get('acertos', 0)
        self.erros = data.get('erros', 0)

        self.questao_atual = None

        Partida.partidas.append(self)

    def proxima_questao(self):
        """
        Método que retorna a próxima questão a ser respondida na partida.
        
        Verifica se ainda houver questões para serem respondidas.
        Se houver, retorna a próxima questão a ser respondida e atualiza o indice.
        Se não houver, retorna None.

        Returns:
            Questao: A próxima questão a ser respondida ou None se todas as questões já foram respondidas.
        """
        if self.indice < len(self.questoes):
            self.questao_atual = self.questoes[self.indice]
            self.indice += 1
            return self.questao_atual

        self.questao_atual = None
        return None

    def progresso(self, resposta_jogador, questao):
        """
        Método que registra o progresso da partida.
        Recebe como parâmetro a resposta do jogador e a questão atual.
        
        Verifica se a questão e a resposta do jogador são válidas. Adiciona um erro.
        Verifica se a resposta do jogador for igual a resposta correta.
        Atualiza o número de perguntas respondidas, acertos e erros.

        Returns:
            bool: True se a resposta do jogador for igual a resposta correta, False nos casos de validação falhar.
        """
        if not questao:
            self.errors.append("Questão inválida ou não encontrada.")
            return False

        correta = questao.get("data", {}).get("respostaCorreta")

        if not resposta_jogador:
            mensagem_resposta = "A resposta é obrigatória para seguir com o jogo."
            if mensagem_resposta not in self.errors:
                self.errors.append(mensagem_resposta)
            return False

        self.perguntas_respondidas += 1

        if resposta_jogador == correta:
            self.acertos += 1
            return True
        
        self.erros += 1
        return False

    @staticmethod
    def pegar_partida(partida_id):
        """
        Método estatico que pega uma partida recebendo seu ID como parâmetro.

        Args:
            partida_id (int): ID da partida a ser pega.

        Returns:
            Partida: A partida com o ID especificado, ou None se nenhuma for encontrada.
        """
        for partida in Partida.partidas:
            if partida.id == partida_id:
                return partida
        return None