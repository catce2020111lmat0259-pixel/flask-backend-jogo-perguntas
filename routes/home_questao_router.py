from flask import Flask

from controllers import home_questao_controller

def adicionar_routes(app: Flask):
    """
    Função que adiciona as rotas relacionadas à home page de questões ao Flask app.

    Adiciona a rota com a requisição para mostrar a página de início das questões.

    :param app: O objeto Flask ao qual as rotas serão adicionadas.
    :type app: Flask
    """
    app.add_url_rule(rule="/questao", endpoint="home_questao", view_func=home_questao_controller.home_questao, methods=["GET"])