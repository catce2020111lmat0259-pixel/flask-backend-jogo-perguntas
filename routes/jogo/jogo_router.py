from flask import Flask

from controllers.jogo import partida_controller

def adicionar_routes(app: Flask):
    """
    Função que adiciona as rotas relacionadas ao jogo ao Flask app.

    Adiciona as rotas com às requisições para iniciar uma partida,
    mostrar o resultado de uma partida, continuar uma partida e finalizar uma partida.

    :param app: O objeto Flask ao qual as rotas serão adicionadas.
    :type app: Flask
    """
    app.add_url_rule(rule="/jogo/partida", endpoint="iniciar_partida", view_func=partida_controller.jogar, methods=["GET"])
    app.add_url_rule(rule="/jogo/resultado", endpoint="resultado_partida", view_func=partida_controller.resultado_partida, methods=["POST"])
    app.add_url_rule(rule="/jogo/resultado/<int:partida_id>", endpoint="mostrar_resultado", view_func=partida_controller.mostrar_resultado, methods=["GET"])
    app.add_url_rule(rule="/jogo/continuar", endpoint="continuar_partida", view_func=partida_controller.continuar_partida, methods=["POST"])
    app.add_url_rule(rule="/jogo/fim", endpoint="fim_partida", view_func=partida_controller.fim_partida, methods=["GET"])