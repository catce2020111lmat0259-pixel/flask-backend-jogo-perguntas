from flask import render_template, request, redirect, url_for

from models.questao.questao_model import Questao

def criar_questao():
    """
    Função que renderiza a página de criação de questão.

    Returns:
        html: Página de criação de questão.
    """
    return render_template('questao/form-criar-questao.html')

def salvar_questao():
    """
    Função que salva uma questão no banco.
    
    Caso o método seja POST, valida e adiciona a questão.
    Data recebe os dados da questão.
    Cria um objeto da classe Questao com os dados da questão passando o data.
    Caso a questão seja adicionada com sucesso, renderiza a página de criação de questão com um contexto de sucesso.
    Caso a questão tenha erros, renderiza a página de criação de questão com um contexto de erro.
    Caso o método seja GET, redireciona para a página de criação de questão.
    
    Returns:
        html: Página de criação de questão com um contexto de sucesso ou erro.
    """
    if request.method == "POST":
        data = request.values
        
        questao = Questao(data=data)
        
        # valida e adiciona a questao validada
        if questao.validate(): 
            questao.adicionar()
            
            context = {
                "questao": questao.data,
                "sucesso": "Questão criada com sucesso!"
            }
            return render_template("questao/form-criar-questao.html", context=context)
        else:
            context = {
                "erros": questao.errors if questao.errors else "Erro desconhecido ao criar a questão."
            }
            return render_template("questao/form-criar-questao.html", context=context)

    return redirect(url_for("criar_questao"))

def listar_questao():
    """
    Função que lista todas as questões do banco.
    
    Cria um objeto da classe Questao e pega todas as questões do modelo.
    Renderiza uma página com todas as questões do banco.
    
    Returns:
        html: Página de lista de questões.
    """
    questoes = Questao.questoes
    context = {
        "questoes": questoes
    }
    return render_template("questao/form-listar-questao.html", context=context)

def editar_questao(id):
    """
    Função que renderiza a página de edição de questão.

    Recebe o id da questão como parâmetro.
    Cria um objeto da classe Questao com o id da questão passando o id.
    Caso a questão seja inválida, redireciona para a página de lista de questões.

    Caso o método seja POST, data recebe os dados da questão.
    Atualiza a questão com os dados da questão passando o data.
    Caso a questão seja atualizada com sucesso, renderiza a página de lista de questões.
    Caso a questão tenha erros, renderiza a página de edição de questão com um contexto de erro.
    
    Args:
        id (int): O id da questão.

    Returns:
        html: Página de edição de questão com um contexto de sucesso ou erro.
    """
    questao = Questao.pegar_questao(id)
    
    if not questao:
        return redirect(url_for("listar_questao"))

    if request.method == "POST":
        data = request.values

        if questao.update(data=data):
            return redirect(url_for("listar_questao"))
        else:
            context = {
                "questao": questao,
                "erros": questao.errors
            }
            return render_template("questao/form-editar-questao.html", context=context)

    context = {
        "questao": questao
    }
    return render_template("questao/form-editar-questao.html", context=context)

def excluir_questao(id):
    """
    Função que renderiza a página de exclusão de questão.

    Recebe o id da questão como parâmetro.
    Cria um objeto da classe Questao com o id da questão passando o id.
    Caso a questão seja inválida, redireciona para a página de lista de questões.
    Renderiza uma página com a questão passando a questão dentro do contexto.
    
    Args:
        id (int): O id da questão.
    
    Returns:
        html: Página de exclusão de questão.
    """
    questao = Questao.pegar_questao(id)
     
    if not questao:
        return redirect(url_for("listar_questao"))
     
    return render_template("questao/form-excluir-questao.html", context={"questao": questao})

def confirmar_exclusao_questao(id):
    """
    Função que confirma a exclusão de uma questão.

    Recebe o id da questão como parâmetro.
    Caso a questão seja inválida, redireciona para a página de lista de questões.
    Caso seja confirmada a exclusão, exclui a questão e redireciona para a página de lista de questões.
    Caso contrário, apenas redireciona para a página de lista de questões.
    
    Args:
        id (int): O id da questão.
    
    Returns:
        html: Página de lista de questões.
    """
    questao = Questao.pegar_questao(id)

    if not questao:
        return redirect(url_for("listar_questao"))

    if request.method == "POST":
        confirmacao = request.form.get("confirmar-exclusao")
        if confirmacao == "Sim":
            questao.excluir()
            
        return redirect(url_for("listar_questao"))

    return redirect(url_for("listar_questao"))