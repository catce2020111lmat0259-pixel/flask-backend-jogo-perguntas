from flask import Flask

from controllers import home_jogo_controller

def adicionar_routes(app: Flask):
    """
    Função que adiciona as rotas relacionadas à home page do jogo ao Flask app.

    Adiciona a rota com a requisição para mostrar a página de início do jogo.

    :param app: O objeto Flask ao qual as rotas serão adicionadas.
    :type app: Flask
    """
    app.add_url_rule(rule="/", endpoint="home", view_func=home_jogo_controller.home_jogo, methods=["GET"])
    app.add_url_rule(rule="/jogo", endpoint="home_jogo", view_func=home_jogo_controller.home_jogo, methods=["GET"])