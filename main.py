from flask import Flask

from routes import home_questao_router
from routes.questao import questao_router

from routes import home_jogo_router
from routes.jogo import jogo_router

app = Flask(__name__)

questao_router.adicionar_routes(app)
home_questao_router.adicionar_routes(app)
home_jogo_router.adicionar_routes(app)
jogo_router.adicionar_routes(app)