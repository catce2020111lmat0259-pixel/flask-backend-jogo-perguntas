class Questao:
    questoes = []
    id_contar = 1
    
    def __init__(self, data):
        """
        Inicializa um objeto da classe Questao com os dados da questão.
        
        Args:
            data (dict): Dicionário com os dados da questão.
        
        Attributes:
            id (int): Número único da questão.
            data (dict): Dicionário com os dados da questão.
            errors (list): Lista de erros.
        """
        
        self.id = Questao.id_contar
        Questao.id_contar += 1 
        
        self.data = data
        self.errors = []
        
    def validate(self):
        """
        Método que valida a questão.
        
        Valida a questão verificando se a pergunta e respostas estão
        preenchidas e se a resposta correta é válida.
        
        Returns:
            bool: True se a questão é válida, False caso contrário.
        """
        
        # validação da pergunta
        pergunta = self.data.get('pergunta')
        
        if not pergunta or not pergunta.strip():
            self.errors.append("A pergunta é obrigatória e não pode estar vazia.")
        else:
            if len(pergunta) < 3:
                self.errors.append("A pergunta deve conter pelo menos 3 caracteres.")
            if len(pergunta) > 300:
                self.errors.append("A pergunta deve conter no máximo 300 caracteres.")
            
        # validação das respostas
        respostas = [
            self.data.get('alternativaA'),
            self.data.get('alternativaB'), 
            self.data.get('alternativaC')
        ]
        
        if not respostas or len(respostas) < 3:
            self.errors.append("A questão deve conter pelo menos 3 respostas.")
        else:
            for resposta in respostas:
                if not resposta or not resposta.strip():
                    if "Todas as respostas devem ser preenchidas." not in self.errors:
                        self.errors.append("Todas as respostas devem ser preenchidas.")
                elif len(resposta) < 1:
                    self.errors.append("As respostas devem conter pelo menos 1 caractere.")
                elif len(resposta) > 100:
                    self.errors.append("As respostas devem conter no máximo 100 caracteres.")
        
        # validação da resposta correta
        resposta_correta = self.data.get('respostaCorreta')
        if resposta_correta not in ['A', 'B', 'C']:
            self.errors.append("É necessário escolher a resposta correta (A, B ou C).")
               
        # se não houver erros, altera os dados da questão com os dados validados
        if len(self.errors) == 0:
            valid_data = {
                'pergunta': pergunta.strip(),
                'respostas': [resposta.strip() for resposta in respostas],
                'respostaCorreta': resposta_correta
            }
            self.data = valid_data
            return True
        return False
    
    def adicionar(self):
        """
        Método que adiciona a questão ao sistema.
        
        Adiciona a questão ao sistema. Pressupondo que a questão foi validada.
        
        Returns:
            bool: True se a questão for adicionada com sucesso.
        """
        Questao.questoes.append(self)
        return True
    
    def listar_questoes(self):
        """
        Método que lista todas as questões cadastradas no sistema.
        
        Retorna a lista de todas as questões cadastradas.
        
        Returns:
            list: Lista de objetos da classe Questao.
        """
        return Questao.questoes
    
    def update(self, data):
        """
        Método que atualiza os dados da questão.

        Limpa a lista de erros.
        Atualiza os dados temporariamente e valida os novos dados.
        Caso a validação falhe, os dados antigos são restaurados.

        Args:
            data (dict): Dicionário com os novos dados da questão.

        Returns:
            bool: True se a atualização for válida e aplicada, False caso contrário.
        """
        self.errors = []

        dados_antigos = self.data.copy()
        self.data.update(data)

        if not self.validate():
            self.data = dados_antigos
            return False

        return True
        
    def excluir(self):
        """
        Método que exclui a questão do sistema.
        
        Cria uma nova lista de questões com todas as questões exceto a questão a ser excluida.
        
        Returns:
            None
        """
        nova_lista_questoes = []
        for questao in Questao.questoes:
            if questao.id != self.id:
                nova_lista_questoes.append(questao)
        Questao.questoes = nova_lista_questoes
        
    @staticmethod
    def pegar_questao(questao_id):
        """
        Método estático que retorna uma questão com base no id.
        
        Percorre a lista de questões e retorna a questão com o id passado.
        
        Args:
            questao_id (int): O id da questão a ser retornada.
        
        Returns:
            Questao: A questão com o id passado ou None se nenhuma questão for encontrada.
        """
        for questao in Questao.questoes:
            if questao.id == questao_id:
                return questao
        return None