from flask import render_template

def home_jogo():
    """
    Função que renderiza a página de início do jogo.
    
    Returns:
        html: Página de início do jogo.
    """
    return render_template('home_jogo.html')