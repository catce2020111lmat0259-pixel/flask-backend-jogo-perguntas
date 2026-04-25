from flask import render_template

def home_questao():
    """
    Função que renderiza a página de início da questão.
    
    Returns:
        html: Página de início da questão.
    """
    return render_template('home_questao.html')
