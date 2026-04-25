import random
from flask import render_template, request, redirect, url_for
from models.questao.questao_model import Questao
from models.jogo.partida_model import Partida
from models.jogo.questoes_teste_model import questoes_testes


def amostra_segura(lista, quantidade):
    """
    Função que retorna uma amostra aleatória segura da lista, para o uso do 'sample'.
    Estamos passando uma quantidade maior do que o tamanho da lista para garantir que a amostra seja segura.

    Args:
        lista (list): Lista que se deseja amostrar.
        quantidade (int): Quantidade de elementos a serem amostrados.

    Returns:
        list: Amostra aleatória da lista.
    """
    return random.sample(lista, min(quantidade, len(lista)))


def montar_questoes():
    """
    Função que monta uma lista de questões para serem usadas no decorrido de uma partida.

    A lista é composta por 5 questões reais e 5 questões de teste, escolhidas aleatoriamente
    e embaralhadas em uma lista única. A lista é embaralhada aleatoriamente para garantir
    que as questões sejam apresentadas em uma ordem aleatória.
    Passamos uma amostra segura e adicionando as questões de teste ao final da lista.

    Returns:
        list: Lista de questões para a partida.
    """
    questoes_reais = amostra_segura(Questao.questoes, 5)
    questoes_teste_escolhidas = amostra_segura(questoes_testes, 5)

    questoes = []

    for questao_real in questoes_reais:
        questoes.append({
            "id": questao_real.id,
            "data": questao_real.data
        })

    for questao_teste in questoes_teste_escolhidas:
        questoes.append(questao_teste)

    random.shuffle(questoes)

    return questoes


def jogar():
    """
    Função que inicia o jogo.

    As questões são montadas e embaralhadas em uma lista de questões para a partida.
    Monta um objeto da classe Partida com os dados da partida e a lista de questões.
    Após montar a partida, escolhe a próxima questão a ser respondida, montando um contexto para a view.

    Returns:
        html: Página de jogo renderizada com as informações da questão para a partida.
    """
    questoes = montar_questoes()

    data = {
        'questoes': questoes,
        'perguntas_respondidas': 0,
        'acertos': 0,
        'erros': 0
    }

    partida = Partida(data=data)
    escolha_questao = partida.proxima_questao()

    context = {
        'partida_id': partida.id,
        'questao': escolha_questao,
        'perguntas_respondidas': partida.perguntas_respondidas,
        'acertos': partida.acertos,
        'erros': partida.erros
    }

    return render_template('jogo/form-jogo-partida.html', context=context)


def resultado_partida():
    """
    Função que processa o resultado de uma questão respondida pelo jogador.

    A função pega o ID da partida, o resposta do jogado, a resposta correta e o ID da questão
    respondida e processa o resultado da questão, verificando se houver erros na resposta do jogado.

    Se houver erros, a função retorna uma página com as informações da questão e dos erros.
    Caso contrário, a função atualiza as informações da partida com o resultado da questão e
    redireciona o jogado para a página de resultado da partida.

    Returns:
        html: Página de erro renderizada com as informações da questão e dos erros, caso haja erros. Ou página de resultado da partida renderizada com as informações da partida.
    """
    partida_id = int(request.form.get('partida_id'))
    partida = Partida.pegar_partida(partida_id)

    resposta_jogador = request.form.get('resposta_jogador')
    resposta_correta = request.form.get('resposta_correta')
    questao_id = int(request.form.get('questao_id'))

    questao_atual = None
    
    for questao in partida.questoes:
        if questao['id'] == questao_id:
            questao_atual = questao
            break

    correta = partida.progresso(resposta_jogador, questao_atual)

    if len(partida.errors) > 0:
        context = {
            'partida_id': partida.id,
            'questao': questao_atual,
            'errors': partida.errors,
            'perguntas_respondidas': partida.perguntas_respondidas,
            'acertos': partida.acertos,
            'erros': partida.erros
        }
        partida.errors = []
        return render_template('jogo/form-jogo-partida.html', context=context)

    partida.data['ultimo_resultado'] = {
        'questao': questao_atual,
        'resposta_jogador': resposta_jogador,
        'resposta_correta': resposta_correta,
        'correta': correta
    }

    return redirect(url_for('mostrar_resultado', partida_id=partida.id))


def mostrar_resultado(partida_id):
    """
    Renderiza a página de resultado da última questão respondida pelo jogadorar.
    
    Se a última questão for nula, redireciona o jogadorar para a página do jogo.
    
    Args:
        partida_id (int): O ID da partida.
    
    Returns:
        html: Página de resultado renderizada com as informações da questão e do desempenho do jogador na partida.
    """
    partida = Partida.pegar_partida(partida_id)
    ultimo = partida.data.get('ultimo_resultado')
    
    if not ultimo:
        return redirect(url_for('jogar'))

    context = {
        'partida_id': partida.id,
        'questao': ultimo['questao'],
        'resposta_jogador': ultimo['resposta_jogador'],
        'resposta_correta': ultimo['resposta_correta'],
        'correta': ultimo['correta'],
        'perguntas_respondidas': partida.perguntas_respondidas,
        'acertos': partida.acertos,
        'erros': partida.erros,
        
        'fim': False
    }

    return render_template('jogo/form-resultado-partida.html', context=context)


def continuar_partida():
    """
    Função que continua a partida para a próxima questão.

    Pega o ID da partida e monta um objeto da classe Partida com os dados da partida .
    Verifica se houve uma próxima questão a ser respondida pela partida.
    Se houver mais uma questão, monta um contexto com as informações da partida e renderiza a página para continuar a partida.
    Se não houver, redireciona o jogador para a página de fim da partida.

    Returns:
        html: Página de jogo renderizada com as informações da questão e da partida continuada.
    """
    partida_id = int(request.form.get('partida_id'))
    partida = Partida.pegar_partida(partida_id)

    escolha_questao = partida.proxima_questao()

    if not escolha_questao:
        return fim_partida(partida=partida)

    context = {
        'partida_id': partida.id,
        'questao': escolha_questao,
        'perguntas_respondidas': partida.perguntas_respondidas,
        'acertos': partida.acertos,
        'erros': partida.erros
    }

    return render_template('jogo/form-jogo-partida.html', context=context)


def fim_partida(partida=None):
    """
    Função que finaliza a partida.

    Verifica se a partida foi passada como argumento.
    Monta um contexto com as informações da partida e renderiza a página de fim da partida.

    Args:
        partida (Partida): Objeto da classe Partida com os dados da partida. (default: None)

    Returns:
        html: Página de fim da partida renderizada com as informações da partida.
    """
    context = {}

    if partida:
        context = {
            'partida_id': partida.id,
            'perguntas_respondidas': partida.perguntas_respondidas,
            'acertos': partida.acertos,
            'erros': partida.erros
        }

    return render_template('jogo/form-fim-partida.html', context=context)