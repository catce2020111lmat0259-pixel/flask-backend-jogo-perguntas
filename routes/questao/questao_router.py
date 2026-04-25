from flask import Flask

from controllers.questao import questao_controller

def adicionar_routes(app: Flask):
    """
    Função que adiciona as rotas relacionadas às questões ao Flask app.

    Adiciona as rotas com as requisições para criar uma questão,
    salvar uma questão, listar todas as questões, editar uma questão,
    excluir uma questão, confirmar a exclusão de uma questão.

    :param app: O objeto Flask ao qual as rotas serão adicionadas.
    :type app: Flask
    """
    app.add_url_rule(rule="/criar", endpoint="criar_questao", view_func=questao_controller.criar_questao, methods=["GET"])
    app.add_url_rule(rule="/criar/salvar", endpoint="salvar_questao", view_func=questao_controller.salvar_questao, methods=["POST"])
    app.add_url_rule(rule="/listar", endpoint="listar_questao", view_func=questao_controller.listar_questao, methods=["GET"])
    app.add_url_rule(rule="/editar/<int:id>", endpoint="editar_questao", view_func=questao_controller.editar_questao, methods=["GET", "POST"])
    app.add_url_rule(rule="/excluir/<int:id>", endpoint="excluir_questao", view_func=questao_controller.excluir_questao, methods=["GET", "POST"])
    app.add_url_rule(rule="/excluir/confirmar/<int:id>", endpoint="confirmar_exclusao_questao", view_func=questao_controller.confirmar_exclusao_questao, methods=["POST"])
    