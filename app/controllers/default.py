from app import app
from app.models.instituicao import Instituicao
from app.database import db



@app.route("/")
def index():
    return 'olá essa é a rota vazia'